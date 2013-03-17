LexTermServer
=============

Development
-----------

### Prerequisites ###
* Python (2.6)
  * If you already have a newer version of python you will need to install 2.6 alongside your
    current version
* pip
  * `easy_install pip`
* virtualenv
  * `pip install virtualenv`

### Setup ###
    mkdir lexTerm && cd lexTerm
    virtualenv -p <path_to_python2.6> --no-site-packages server 
    cd server
    source bin/activate
    pip install django==1.4
    git clone git@github.com:LexTerm/LexTermServer.git

### Run it ###
    cd LexTermServer
    python manage.py runserver

