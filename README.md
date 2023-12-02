# api-django-dtr



Run pipenv install --dev
Then pipenv shell
Development
Default settings for this project are development settings. Those can be edited in file MAIN/settings/development.py

To run Django project with those settings run: python manage.py runserver

Production (Running Django with production settings, to deploy this application look at Running with docker)
Note: WSGI and ASGI applications will use this settings, to change it edit asgi.py or wsgi.py and change DJANGO_SETTINGS_MODULE

Production settings are using environment variables, to edit this behaviour edit the file MAIN/settings/development.py

To run Django project with those settings run: python manage.py runserver --settings=MAIN.settings.production

Running with docker
Firstly change environment variables inside application.env and database.env

Run and build docker container docker-compose up -d --build Now you will have Django application on port 8000. Open browser and type: localhost:8000

Installed apps
Whitenoise - Serving static files
Django Debug Toolbar - Toolbar for debug purposes
