---
layout: post
---
<iframe src="http://ghbtns.com/github-btn.html?user=jakobadam&repo=bootstrap-uploadprogress&type=watch&count=true" allowtransparency="true" frameborder="0" scrolling="0" width="100px" height="20px"></iframe>

*Progress bar on form uploads using a Twitter Bootstrap modal.*

[Bootstrap UploadProgress](https://github.com/jakobadam/bootstrap-fileprogress) is a jQuery plugin that progressively enhances browsers, by popping up a modal with an upload progress bar on form submission. The plugin is both simple, unobtrusive and very easy to add, even to existing forms.

<iframe src="https://player.vimeo.com/video/129529600?title=0&byline=0&portrait=0" width="530" height="203" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

The plugin uses the following advanced features of `XMLHttpRequest`: `FormData` and `ProgressEvent`. These are supported by all modern browsers according to [caniuse.com](http://caniuse.com/#feat=xhr2)

## Example for the impatient
Preconditions:

* Twitter Bootstrap
* jQuery

Add to HTML:

<small>
<?prettify?>
```html
<script type="text/javascript" src="js/bootstrap-fileprogress.js"> </script>
```
</small>

Decorate form:

<small>
<?prettify?>
```javascript
$("#form").uploadprogress({redirect_url: '/'});
```
</small>

Result:
When a user submits the form a modal with upload progress pops up and the form is submitted through `XHR` in the background. Uploads can be cancelled by closing the modal. On successful uploads the browser is redirected to `redirect_url`. 

Note: If you have validation logic on the backend, in addition to the changes above, you must make a tiny change on the backend.

## Displaying form validation errors
Web frameworks usually handle validation errors of the form by rendering the page again  including the errors in the HTML. In order for UploadProgress to know when the form is successfully submitted, the backend must set an appropriate HTTP status on the response.

On `HTTP 422`'s UploadProgress closes the modal and replaces the form on the page with the relevant one in the response. On `HTTP 200` the browser is redirected to `redirect_url`. This fits in naturally with most web frameworks, and requires only a tiny addition to the backend.

## Django File Upload with progress bar example
This example uses Django, but should be similar in other frameworks. Taking the Django backend logic from the Django documentation [working with forms](https://docs.djangoproject.com/en/1.8/topics/forms/#the-view) as starting point, supporting validation errors in UploadProgress is just a matter of setting the response status to `HTTP 422` on form validation errors:

<?prettify?>
``` python
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm

def get_name(request):
	status = 200
    if request.method == 'POST':
        form = NameForm(request.POST, request.FILES)
        if form.is_valid():
	        form.save()
            return HttpResponseRedirect('/thanks/')
        else:
            status = 422 # signal error to UploadProgress
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form}, status=status)
```

Code is available on [GitHub](https://github.com/jakobadam/bootstrap-uploadprogress) and licensed under the MIT License. Feedback and contributions are always welcome.

<script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
