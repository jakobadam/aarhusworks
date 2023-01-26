---
title: "Smooth scrolling in Angular – the simple way"
---

Smooth scrolling is something all UXers want. 

Optimally I would use the Angular [ViewportScroller](https://github.com/angular/angular/blob/main/packages/common/src/viewport_scroller.ts),
but it doesn't support smooth scrolling. Instead, we create our own scroll service.

Fortunately it has become really easy to implement, since smooth scrolling
has native support in all major browsers.

Even though, there's an [almost 100% supported](https://caniuse.com/?search=scrollTo) `Element.scrollTo`, 
the safe bet is to go with `Window.scrollTo`.

Going with `Window.scrollTo`, for the wider support, also means we must convert from the viewport position
(think position in the browser window) of the element obtained through `getBoundingClientRect`, to a document position. 
However, that's pretty straightforward:

```ts
const elTopViewportPosition = targetEl.getBoundingClientRect().top;
const elTopAbsolutePosition = elTopViewportPosition + this._document.documentElement.scrollTop;
```

And when we have the absolute position, the `scrollTo` with a smooth argument can be used:

```ts
this._window?.scrollTo({
  top: elTopAbsolutePosition + offset,
  behavior: 'smooth',
});
```

At last, for assistive technology / tabbing to work the element jumped to needs to be focused.

```ts
targetEl.focus();
```

The complete scroll service:

```ts
import { DOCUMENT } from '@angular/common';
import { Inject, Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class ScrollService {

  private _window: Window | null;

  constructor(@Inject(DOCUMENT) private _document: Document) {
    this._window = _document.defaultView;
  }

  scrollTo(id: string, offset = 0) {
    const targetEl: HTMLElement | null = this._document.querySelector('#' + id);
    if (!targetEl || !this._window) {
      return;
    }

    const elTopViewportPosition = targetEl.getBoundingClientRect().top;
    const elTopAbsolutePosition = elTopViewportPosition + this._document.documentElement.scrollTop;
    
    this._window.scrollTo({
      top: elTopAbsolutePosition + offset,
      behavior: 'smooth',
    });
    
    targetEl.focus();
  }
}
```

## Demo
<iframe style="height:500px; width: 100%" src="https://stackblitz.com/edit/angular-ivy-ds2bwn?embed=1&file=src/app/scroll.service.ts&view=preview"></iframe>

## Links

* [MDN - getBoundingClientRect](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect)
* [MDN - scrollTo](https://developer.mozilla.org/en-US/docs/Web/API/Window/scrollTo)




