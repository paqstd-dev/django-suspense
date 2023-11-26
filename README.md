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
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["suspense.templatetags.suspense"],
        },
    },
]
```
If you choose not use it as a built-in, you will need to add `{% load suspense %}` to the top of your template whenever you want to use suspense.

### 2. Add `suspense` to `urls.py`:
This is necessary because some parts of the pages will be loaded asynchronously (via http).
```python
from django.urls import include, path


urlpatterns = [
    ...,
    path('/_suspense/', include('suspense.urls'))
]
```

### 3. Create view with slow lazy load object:
Because django executes database queries lazily, they may sometimes not work as expected. Let's try to create a very slow but lazy object and write a view function:
```python
# app/views.py
def view(request):
    def obj():
        import time

        i = 0
        while i < 10:
            yield i
            i += 1
            time.sleep(1)

    return render(request, 'template.html', {'obj': obj})
```

### 4. Use `suspense` in your template:
Let's now add the output of the received data to the template. At this point, we still haven't made a database query, so we can easily and quickly show the template right away.
```html
{% load suspense %}

<div class="list">
    {% suspense %}
        {% fallback %}
            <div class="skeleton">Loading ... </div>
        {% endfallback %}

        <ul>
            {% for data in obj %}
                <li>{{ data }}</li>
            {% endfor %}
        </ul>
    {% endsuspense %}
</div>
```
Once obj is ready for use, we will show it. But until it is ready, fallback works. While we are waiting for the data to be displayed, a request is made on the client side.

### 5. Hooray! Everything is ready to use it.


## Contributing
If you would like to suggest a new feature, you can create an issue on the GitHub repository for this project.
Also you can fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
