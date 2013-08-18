LexTermServer
=============

Development
-----------

### Prerequisites ###
* Python (2.7)
* pip
  * `easy_install pip`
* virtualenv
  * `pip install virtualenv`

### Setup ###
    mkdir lexTerm && cd lexTerm
    virtualenv --no-site-packages server 
    cd server
    source bin/activate
    git clone git@github.com:LexTerm/LexTermServer.git lexTerm
    cd lexTerm
    pip install -r requirements.txt
    ./manage.py syncdb

### Run it ###
    ./manage.py runserver

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

