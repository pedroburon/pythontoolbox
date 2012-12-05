The Python Toolbox Project
==========================

[Running on heroku](http://blooming-inlet-1605.herokuapp.com/)


Installing for development
==========================

Fork me! then...

    $ git clone git@github.com:YOURACCOUNT/pythontoolbox.git
    $ cd pythontoolbox

Using your virtualenvironment

    $ pip install -r requirements.txt
    $ ./manage.py syncdb

Add environment variables to .env

    $ cat >.env <<EOM
    PORT=8000
    DEBUG=True
    SQL_LOGGING=True
    EOM

Run with [honcho](https://github.com/nickstenning/honcho)

    $ honcho start

if you want autoreload

    $ honcho run ./manage.py runserver
