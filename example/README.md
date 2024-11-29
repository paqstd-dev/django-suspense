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
Now that everything is ready, you can start the asgi server:
```bash
PYTHONPATH=$PWD/../ python -m uvicorn example.asgi:application
```
