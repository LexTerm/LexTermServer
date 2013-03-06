LexTermServer
=============

Development
-----------

### Prerequisites ###
* Python (2.7)
* pip (`easy_install pip`)
* virtualenv (`pip install virtualenv`)

### Setup ###
    mkdir lexTerm && cd lexTerm
    virtualenv server --no-site-packages
    cd server
    source bin/activate
    pip install django
    git clone git@github.com:LexTerm/LexTermServer.git

### Run it ###
    cd LexTermServer
    python manage.py runserver

