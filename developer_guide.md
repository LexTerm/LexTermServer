Developer Guide for the LexTerm Project
=======================================

Working on the server
---------------------

Python development should always be done in a virtual environment to avoid dependency issues.
Instructions for setting up a virtual environment can be found in the [readme](./README.md). I would
also recommend installing [virtualenvwrapper][], which makes managing virtual environments easier.
By using virtual environments, along with the [requirements file](./requirements.txt), every
developer and every production environment will be using the same versions of all dependencies.
Simply issuing a `pip install -r requirements.txt` with the virtual environment activated will
install or update all the dependencies.

[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/

The LexTerm server has been developed using [Django][], and [Django REST Framework][](DRF). The websites
for both projects provide very valuable documentation. The project is structured like a regular
django project, but DRF provides many useful shortcuts to speed up development. Currently, the
LexTerm system uses sqlite as the database backend for its simplicity, but Django makes this easy to
swap out.

[django]: https://www.djangoproject.com/
[django REST framework]: http://django-rest-framework.org/

There are three main apps that make up the LexTerm project. The `lex` app handles the lexicographic
data, with the `Language` model forming the foundation for all the other lex models. The `term` app
handles terminological data, with the `Concept` model as the foundation for the rest of the term
models. The `tbx` app contains views for TBX validation, import, and (eventually) export. The TBX
views use [lxml][], a Python binding for the libxml2 C library, to parse TBX files

[lxml]: http://lxml.de/

Working on clients
------------------

The LexTerm server is designed to be completely agnostic about the client that is used with it. It
provides a modern web API with all the infrastructure needed to support it. The API is fully
documented at [apiary][], so that should be the main reference when developing a LexTerm client. 

[apiary]: http://docs.lexterm.apiary.io/

The LexTerm API has been developed with [RESTful][] principles in mind. In particular, it has been
designed so that clients have to know as little as possible about the server. For example, making
the following request with cURL:

    curl --include "http://lexterm.apiary.io/api/lex/lang/eng"

Will return the following response:

    {
        "name": "English",
        "langCode": "eng",
        "_links": {
            "self": "lexterm.apiary.io/api/lex/lang/eng",
            "classes": "lexterm.apiary.io/api/lex/lang/eng/classes",
            "enums": "lexterm.apiary.io/api/lex/lang/eng/enums",
            "lexemes": "lexterm.apiary.io/api/lex/lang/eng/lexemes",
            "reps": "lexterm.apiary.io/api/lex/lang/eng/reps"
        }
    }

All the keys in the `_links` object contain fully-qualified urls so the client doesn't have to know
how to construct urls for each linked resource. This has the additional advantage of allowing much
of the API to change without having to change the client implementation. Another aspect of
implementing a RESTful design is that the standard [CRUD][] operations have been appropriately
mapped to HTTP methods (i.e., create ==> POST, retreive ==> GET, update ==> PUT, destroy ==> DELETE)

[RESTful]: http://en.wikipedia.org/wiki/RESTful
[CRUD]: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete

