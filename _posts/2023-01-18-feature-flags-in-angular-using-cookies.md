# Feature flags in Angular using cookies

These days most modern software projects are turning towards
trunk-based development, letting all the perils of git flow be a thing
of the past.

One of the pre-requisites for going trunk-based is the ability to hide
un-released, but still in production, features from
end-users. 

This concept is called feature flags in broadly 
terms, and more specific release flags. There are other types of
feature flags: experimental flags, operational toggles, permission
toggles etc., but none of those are requirements for going
trunk-based. So here we focus on release flags.

For more on feature flags see: https://www.martinfowler.com/articles/feature-toggles.html

## Requirements

Albeit, the concept being enormously simple, in essence just an if
statement, it's possible to go all-in on feature flag complexity.
Instead of going into a rabbit hole of feature flag features, this
post describes the implementation of a dead simple release flag
approach with the following characteristics:

1. easy to add for developers
2. easy to toggle for non-developers
3. easy to cleanup for developers
4. easy to use from the Angular front-end
5. easy to use from the back-end
6. no external deps
7. free

Here's a [demo](https://angular-ivy-t6atw6.stackblitz.io), and a
[stackblitz](https://angular-ivy-t6atw6.stackblitz.io).

Note: This post is about the Angular side, and I've omitted the back-end implementation from the description. 

## The API end-goal

The most simple use case for Angular templates is a structural directive
that only shows content if some flag is enabled.

```html
<span *featureFlag="'flag-1'">On</span>
```

Don't worry about 'flag-1' being a string, we'll use the powerful
literal types of Typescript to ensure compile time safety.

For simple template if-else logic, I often find myself inverting the
condition of `ngIf`s. Our directive should also support that:

```html
<span *featureFlag="'!flag-1'">Off</span>
```

When the `featureFlag` directive is present on a larger block of code,
just like for `ngIf`s, it can be useful to convey clearly that there is an
accompanying `else` part to the `if`. Similar, to `ngIf` we'll specify that via an
optional `else` clause.

```html
<span *featureFlag="'flag-2'; else feature2off">On</span>

<ng-template #feature2off>Off</ng-template>
```

Of course, we also need to feature flag logic in non-html Angular; a root injected service is used for that.

```ts
const isActive = this._featureFlagService.isActive(flag);
```

### Enabling the flag

To be completely back-end and front-end tech-stack agnostic, cookies are used for the feature flag state.

A flag is enabled as follows from the front-end:

```js
document.cookie = 'featureflag:flag-1=true' // + browser reload
```

In addition, I envision through a back-end middleware through the use
of query params:

```http
GET /?featureflag:flag-1=true
```

And disabled, by:
```js
document.cookie = 'featureflag:flag-1=false'
```

Or via the backend:
```http
GET /?featureflag:flag-1=false
```

Of course, the cookie can also 'just' be removed.

These actions by intention, enables the feature flag for the current
user's session only. All flags are inherently disabled by default, however, some middleware
back-end could default the flag to true instead, but for release flags that's not needed.

## Implementation

### Angular feature flag service

There are three important public methods of the feature flag service underneath.
1) `activate` and 2) `deactivate` - sets the cookie for the given
feature flag with the proper values, and 3) `isActive` - that reports
whether the given feature flag's corresponding cookie value is true.

```ts
const FEATURE_FLAG_COOKIE_KEY_PREFIX = 'featureflag';

@Injectable({
  providedIn: 'root',
})
export class FeatureFlagService {
  constructor(private _cookieService: CookieService) {}

  activate(featureFlag: FeatureFlag) {
    const flagCookieValue = this._getCookieKey(featureFlag);
    return this._cookieService.set(flagCookieValue, 'true');
  }

  deactivate(featureFlag: FeatureFlag) {
    const flagCookieValue = this._getCookieKey(featureFlag);
    // or expire the cookie...
    return this._cookieService.set(flagCookieValue, 'false');
  }

  /**
   * Whether the given feature flag is present in cookies.
   */
  isActive(featureFlag: FeatureFlag): boolean {
    const flagCookieValue = this._getCookieKey(featureFlag);
    return this._cookieService.get(flagCookieValue) === 'true';
  }

  private _getCookieKey(featureFlag: FeatureFlag) {
    return FEATURE_FLAG_COOKIE_KEY_PREFIX + ':' + featureFlag;
  }
}
```

The service heavily relies on a cookie service, which is not really
important for this post, but available here
[cookie.service.ts](https://stackblitz.com/edit/angular-ivy-t6atw6?file=src%2Fapp%2Fcookie.service.ts)

The type, `FeatureFlag`, of the arguments to those service methods is
quite interesting though.

```ts
export type FeatureFlagName = 'flag-1' | 'flag-2';
type FeatureFlagNameInverted = `!${FeatureFlagName}`;

export type FeatureFlag = FeatureFlagName | FeatureFlagNameInverted;
```

`FeatureFlagName` is a union of [string literal
types](https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html
).

And `FeatureFlagNameInverted` uses [template literal
types](https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html)
to add a `!` in front of the string literal types, creating an additional two types in the example above. 

At last, the two are unioned together. This makes it possible to have
only one place to add / remove flags in the code, and gives us compile
time guarantees for our templates, assumed that [template type
checking](https://angular.io/guide/template-typecheck#template-type-checking)
is enabled.

For example, underneath 'flag-1' is removed, but still used in a template.
![compile time error when flag is missing](/assets/feature-flags-in-angular-directive-and-service-using-cookies-compile-error.png)

The feature flag service is synchronous. That means, it's
simple, but dynamic updates of the UI based on the value of the cookie
is not supported - with other words, the browser needs a refresh for
flag changes to materialize.

### Angular structural directive, `*featureFlag`
```ts
@Directive({
  selector: '[featureFlag]',
  standalone: true,
})
export class FeatureFlagDirective {} 
```

The [feature
flag](https://stackblitz.com/edit/angular-ivy-t6atw6?file=src%2Fapp%2Ffeatureflag.directive.ts)
directive is similar to
[ngIf](https://github.com/angular/angular/blob/main/packages/common/src/directives/ng_if.ts). But,
instead of a boolean expression our directive takes a string literal
type defined above, e.g., `'flag0'` or `'!flag0'`.

```ts
  @Input() set featureFlag(featureFlag: FeatureFlag) {
    if (featureFlag.charAt(0) === '!') {
      this._inverted = true;
      this._featureFlag = featureFlag.slice(1) as FeatureFlag;
    } else {
      this._featureFlag = featureFlag as FeatureFlag;
    }
    this.updateView();
  }
```

Since the directive has support for an `else` clause, there's also an else
'template' input binding.

```ts
  @Input() set featureFlagElse(templateRef: TemplateRef<any>) {
    this._elseTemplateRef = templateRef;
    this.updateView();
  }
```

On `updateView` the feature flag service is utilized for getting the
feature flag value. Based on that value the directive displays the
corresponding template, taking into consideration whether the flag was
inverted or not.


```ts
  updateView() {
    const isFeatureActive = this._featureFlagService.isActive(
      this._featureFlag
    );
    this._clearViewContainer();
    this._createView(isFeatureActive);
  }

  private _createView(isFeatureActive: boolean) {
    let showThen = this._inverted ? !isFeatureActive : isFeatureActive;
    if (showThen) {
      this._createThenView();
    } else if (this._hasElseTemplate) {
      this._createElseView();
    } else {
      // don't show anything
    }
  }
```

## Conclusion

And that's it, a simple, dependency free, easy to use, Angular cookie based feature flag.

However, one thing was omitted from this post. 
That was the backend. But, since the approach is based on cookies, middleware of any web framework, would be a perfect fit to implement the server side.

To be concrete, that could be realised in C# through [IHttpModule](https://learn.microsoft.com/en-us/previous-versions/aspnet/ms227673(v=vs.100)), or Django using [middleware](https://docs.djangoproject.com/en/dev/topics/http/middleware/)

The implementation of the back-end would also check-off the 'easy to toggle for non-developers' requirement, but the description of such a thing is for another day...





