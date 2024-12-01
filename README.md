# Django Suspense
[![PyPI version](https://img.shields.io/pypi/v/django-suspense)](https://pypi.python.org/pypi/django-suspense/)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/django-suspense.svg)](https://pypi.python.org/pypi/django-suspense/)
[![PyPI Supported Django Versions](https://img.shields.io/pypi/djversions/django-suspense.svg)](https://pypi.python.org/pypi/django-suspense/)
[![Coverage)](https://codecov.io/github/paqstd-dev/django-suspense/graph/badge.svg)](https://app.codecov.io/github/paqstd-dev/django-suspense)

Django Suspense is small package to easily display a fallback in templates until children have finished loading.


## Quick start

### 1. Install package:
To get started, install the package from [pypi](https://pypi.org/project/django-suspense/):
```bash
pip install django-suspense
```

Now you can add `suspense` to your django project. Change your `INSTALLED_APPS` setting like this:
```python
INSTALLED_APPS = [
    ...,
    "suspense",
]
```

Optionally, you can specify `suspense` as builtins and this will be available in any of your templates without additionally specifying `{% load suspense %}`:
```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # ... list of default processors
            ],
            "builtins": ["suspense.templatetags.suspense"], # <--
        },
    },
]
```
If you choose not use it as a built-in, you will need to add `{% load suspense %}` to the top of your template whenever you want to use suspense.


### 2. Create view with slow lazy load object:
Because django executes database queries lazily, they may sometimes not work as expected. Let's try to create a very slow but lazy object and write a view function:
```python
from suspense.shortcuts import render

# app/views.py
def view(request):
    def obj():
        import time

        time.sleep(1)
        return range(10)

    return render(request, 'template.html', {'obj': obj})
```

### 3. Use `suspense` in your template:
Let's now add the output of the received data to the template. At this point, we still haven't made a database query, so we can easily and quickly show the template right away.
```jinja
{% load suspense %}

<ul>
    {% suspense %}
        {% fallback %}
            <li class="skeleton">Loading ... </li>
        {% endfallback %}

        {% for data in obj %}
            <li>{{ data }}</li>
        {% endfor %}
    {% endsuspense %}
</ul>
```
Once obj is ready for use, we will show it. But until it is ready, fallback works. While we are waiting for the data to be displayed, a request is made on the client side.

> Suspense does not add additional DOM elements after rendering the final result. That's why syntactically the code above will be valid.

### 4. Hooray! Everything is ready to use it.


## Troubleshooting

### Safari delay in rendering

On Safari if your webpage is very light/simple, you may experience a delay in rendering.

Ex: the page renders only after some django-suspense or all content is downloaded.

WebKit has an issue with streaming responses requiring a certain amount of visible content before to actually start rendering.

See [webkit issue #252413](https://bugs.webkit.org/show_bug.cgi?id=252413)

If you are experiencing this issue, you can use the additional `{% webkit_extra_invisible_bytes %}` template tag to add a few extra invisible bytes in Safari.

```jinja
{% load suspense %}

{% webkit_extra_invisible_bytes %}
```

By default the `webkit_extra_invisible_bytes` adds 200 bytes but you can specify a different amount:

```jinja
{% webkit_extra_invisible_bytes 300 %}
```

### Content Security Policy (CSP) nonce error because of `strict-dynamic`

If you are using a Content Security Policy (CSP) with `nonce` and [`strict-dynamic`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src#strict-dynamic), you may need to add the `nonce` attribute to the script tag.

You can override the `suspense/replacer.html` template and add the `nonce` attribute to the script tag.

With [django-csp](https://django-csp.readthedocs.io/en/latest/nonce.html#middleware):

```jinja
{% extends "suspense/replacer.html" %}

{% block script_attributes %}nonce="{{request.csp_nonce}}"{% endblock %}
```


## Contributing
If you would like to suggest a new feature, you can create an issue on the GitHub repository for this project.
Also you can fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
