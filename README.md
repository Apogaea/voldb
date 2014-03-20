## Apogaea Volunteer Database

[![Build Status](https://travis-ci.org/Apogaea/voldb.png)](https://travis-ci.org/Apogaea/voldb)

### Development Environment Setup

This is assuming a MacOS X or Linux development environment, with Python 2.7 installed.
This will use virtualenv to manage a Django v1.7 project.


1. **Install postgres**  

  We need to install `postgresql`.

  ```bash
  $ brew install postgresql  # Mac
  $ sudo apt-get install postgresql  # Ubuntu/Linux
  ```

1. **Install virtualenv**  
  
  First ensure python is installed (it likely is already): 
 
  ```bash
  $ brew install python --with-brewed-openssl # Mac
  $ sudo apt-get install python # Ubuntu Linux (I think this will get latest 2.x)
  
  ```   
  ```bash
  $ pip install virtualenv           # MacOS
  $ sudo apt-get isntall virtualenv  # Ubuntu Linux
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
