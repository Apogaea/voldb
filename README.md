## Apogaea Volunteer Database

[![Build Status](https://travis-ci.org/Apogaea/voldb.png)](https://travis-ci.org/Apogaea/voldb)

### Development Environment Setup

This is assuming a MacOS X or Linux development environment, with Python 2.7 installed.
This will use virtualenv to manage a Django v1.7 project.


1. **Install postgres**  

  We need to install `postgresql` and `memcached`.

  ```bash
  $ brew install postgresql memcached libmemcached  # Mac
  $ sudo apt-get install postgresql python-memcache memcached  # Ubuntu/Linux
  ```
 
  On Mac, I also had to add `pg_config` to the path for pip to install requirements correctly:
  ```
  export PATH=$PATH:/opt/local/lib/postgresql92/bin # Optionally add this to .bashrc
  ```

1. **Install virtualenv**  
  
  First ensure python is installed (it likely is already): 
 
  ```bash
  $ brew install python --with-brewed-openssl # Mac
  $ sudo apt-get install python # Ubuntu Linux (I think this will get latest 2.x)
  
  ```   
  ```bash
  $ pip install virtualenv           # MacOS
  $ sudo apt-get install virtualenv  # Ubuntu Linux
  ```
  
1. **Clone the Apogaea VolDB Git repository**

  ```bash
  $ git clone git@github.com:Apogaea/voldb.git
  ```

3. **Create a virtual environment and activate it**
  
  ```bash
  $ cd voldb
  $ virtualenv env
  $ source env/bin/activate
  ```

4. **Install application dependencies**
  
  ```bash
  $ pip install -r requirements.txt
  ```

5. **Setup your database**

  ```bash
  $ ./manage.py syncdb
  ```

6. **Start the Django web application**

  This will start a local webserver running on http://localhost:8000

  ```bash
  $ ./manage.py runserver
  ```
  This will allow you to develop and reload your changes live in the browser.
  
  Or to load the development webserver such that other devices on the local
  network (e.g. tablets) can access it:
  
  ```bash
  $ python manage.py runserver '[::]:8000'
  ```

### Heroku Stuff

The volunteer database, while fundamentally agnostic to the hosting
environment, is at the time of writing this, hosted on heroku.  The best way as
a developer to interact with this is via the heroku cli.

https://devcenter.heroku.com/articles/heroku-command

Here are some basics for how to do *stuff* on heroku.  This is very barebones
as, much more detailed instructions are availble on the heroku docs.  Most of
these docs assume that you know some of the internals of managing a django
project.


####Deploying

To deploy the latest version from the master branch.

```bash
$ git push heroku master
```

To deploy from a branch that isn't master.
```bash
$ git push heroku some_other_branch:master
```

Often deploying may involve running certain migrations.

```bash
$ heroku run python manage.py migrate
```

####Interactive Shell

Similar to running migrations, you may want to jump into a python shell for
various reasons.

```bash
$ heroku run python manage.py shell
```

####Configuration

The majority of the app is configured via environment variables.  You can see a
full list of them by running the following.

```bash
$ heroku config
```

Or set/change one

```bash
$ heroku config:set DJANGO_DEBUG='True'
```

####Logs

You can see what's going on by tailing the logfiles.

```bash
$ heroku logs -t
```
