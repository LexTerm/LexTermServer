LexTermServer
=============

Development
-----------

### Prerequisites ###
* Python (2.7)
* pip
* virtualenv (virtualenvwrapper is recommended)

### Setup ###

Set up a python virtual environment however you want. Here's a simple way to do that:

    mkdir lexTerm && cd lexTerm
    virtualenv --no-site-packages server
    cd server
    source bin/activate

Clone the source repository from GitHub:

    git clone git@github.com:LexTerm/LexTermServer.git lexTerm
    cd lexTerm

Install all python dependencies in the virtual environment

    pip install -r requirements.txt

Copy settings template
    
    cp lexTerm/local_settings.py.tmpl lexTerm/local_settings.py
    
Edit local_settings.py to configure your database and other settings

Initialize the database

    ./manage.py syncdb --all
    ./manage.py migrate --fake

### Run it ###

    ./manage.py runserver

API Documentation
-----------------

On a running server, navigate to /api to browse the API.
Further documentation will be forthcoming.

Production
----------

### Setup ###
* ssh onto the server
* create a virtual environment
* `git clone https://github.com/LexTerm/LexTermServer.git lexTerm`
* `cd lexTerm`
* `mkdir static`
* In the webserver document root do `ln -s path/to/lexTerm/static static`
* follow the django instructions [here]
  (https://docs.djangoproject.com/en/1.5/howto/deployment/fastcgi/#running-django-on-a-shared-hosting-provider-with-apache)

### Deploy ###
* to update, simply `git pull` in the repository
* make sure to run `./manage.py syncdb` if any changes were made to database schemas

