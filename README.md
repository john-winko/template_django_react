# Full Stack from scratch steps

## Notes
- Replace "app" with your app / api / backend name
- Replace "proj" with the django project name you want to use

## Create React Frontend
Starting from a blank folder
~~~
npx create-react-app .
~~~
~~~
npm install watch axios react-router-dom
~~~

## Create Django Backend
~~~
python -m venv .venv
~~~
### This is for windows... use the correct activate on mac/linux
~~~
.venv/scripts/activate.ps1
~~~
~~~
pip install django djangorestframework psycopg2 psycopg2-binary
~~~
~~~
django-admin startproject proj .
~~~
~~~
python manage.py startapp app
~~~

## Make sure everything runs as is
### Verify django
~~~
python manage.py runserver
~~~
### Verify react
~~~ 
npm run start (verified react runs)
~~~

## Update proj/settings.py
~~~ python
import os

...

INSTALLED_APPS = [
    ...
    'app', 
    'rest_framework'
]

...

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "build/static"), # your static/ files folder
]
~~~

## Update the app/views.py
~~~ python
from django.http import HttpResponse

# Create your views here.
def send_the_homepage(request):
    theIndex = open('build/index.html').read()
    return HttpResponse(theIndex)
~~~

## Update proj/urls.py
~~~ python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls"))
]
~~~

## Update app/urls.py
~~~ python
from django.urls import path 
from . import views


urlpatterns = [
    path('', views.send_the_homepage),
]
~~~

## update package.json (Windows)
~~~ json
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "watch": "watch \"npm run build && copy manage.py+\" ./src"
  },
~~~

## update package.json (Mac/Linux)
~~~ json
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "watch": "watch \"npm run build && copy manage.py+\" ./src"
  },
~~~

## Update .gitignore as necessary
