# Posts App

## Getting Started
To get started, activate the virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Next you need to install all dependencies:
```bash
pip install -r requirements.txt
```

And the last step is to apply Django migrations:
```bash
python manage.py migrate
```

Now we can start the server!

## Populating the Database
A database dump was specially prepared for quick launch. You can apply it by running the command:
```bash
python manage.py loaddata example.db.json
```

This command will add several posts with title and content.

## Run server
Now that everything is ready, you can start the local server:
```bash
PYTHONPATH=$PWD/../ ./manage.py runserver
```


# ASGI

## Install unicorn
```bash
pip install -r requirements.txt uvicorn
```

## Run ASGI server

```bash
PYTHONPATH=$PWD/../ python -m uvicorn example.asgi:application
```

## Test the async view

You must use https://127.0.0.1/async/ or https://127.0.0.1/async/class-view/ to test the async views.
