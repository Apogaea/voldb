## Apogaea Volunteer Database

[![Build Status](https://travis-ci.org/Apogaea/voldb.png)](https://travis-ci.org/Apogaea/voldb)

### Contributing

See the [Contribution Guide](CONTRIBUTING.md)

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
  ```bash
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
  $ pip install -r requirements-dev.txt
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

### Running the tests

The tests are run via tox.

```bash
$ tox
```

To run a only the flake8 tests

```bash
$ tox -e flake8
```

To run a only the python tests

```bash
$ tox -e py27-django17
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


# V2 API

## Departments: `/api/v2/departments/`

```json
{
    "count": 123,
    "data":[
        {
            "id":1,
            "name":"DPW",
            "description":"Deparment of Public Works",
            "leads":[
            ],
            "liaison":null
        },
        {
            "id":2,
            "name":"Rangers",
            "description":"somehing something peaceful mediation",
            "leads":null,
            "liaison":null
        },
        ...
    ]
}
```

- **id**: The primary key of the department.
- **name**: The department name.
- **description**: The department description.
- **leads**: Either `null` or an array of user ids.

## Roles: `/api/v2/roles/`

```json
{
    "prevous": null,
    "next": "http://127.0.0.1:8000/api/v2/roles/?page=2",
    "count": 123,
    "data":[
        {
            "id":1,
            "department":2,
            "name":"the name of the role",
            "description":"The description of the role"
        },
        {
            "id":1,
            "department":2,
            "name":"the name of the role",
            "description":"The description of the role"
        },
        ...
    ]
}
```

- **id**: The primary key of the role.
- **department**: The primary key of the department this role belongs to.
- **name**: The name of this role.
- **description**: The department description.

## Shifts: `/api/v2/shifts/`

```json
{
    "prevous": null,
    "next": "http://127.0.0.1:8000/api/v2/shifts/?page=2",
    "count": 123,
    "data":[
        {
            "id":1,
            "role":2,
            "start_time":1418947200,
            "shift_length":3,
            "owner":4
        },
        {
            "id":2,
            "role":2,
            "start_time":1418947200,
            "shift_length":3,
            "owner":4
        },
        ...
    ]
}
```

- **id**: The primary key of the shift.
- **role**: The primary key of the role this shift belongs to.
- **start_time**: The timestamp of the time the shift starts at.
- **shift_length**: The length in units of time (currently hours) of the shift.
- **owner**: The primary key of the shifts owner.

## Shift Claiming: `/api/v2/shifts/:id/`

A `PUT` or `PATCH` to the detail endpoint for a shift will allow you to *claim*
it by specifying the claiming user's id as the `owner` field in the request
data.

You cannot modify a shift that is not claimed by you.

Shifts with no owner can be claimed by anyone.

## Shift Grid `/api/v2/shift-grid/?s=1&s=2&s=3`

Returns the shifts in grid format.

[Full Example Response](https://gist.github.com/pipermerriam/929a4b3e32277c082f67)


The response is structured as follows.

For each combination of *date* and *shift_length*:

```json
{
  "date": timestamp,
  "length": shift_length,
  "grid": [<column_object>, ...],
}
```

- **date**: timestamp for what date this grid data is for.
- **length**: the length of all shifts in this grid.
- **grid**: the grid data (*see below*)


```json
{
  "columns": 1,
  "open_on_left": false,
  "open_on_right": false,
  "start_time": timestamp,
  "end_time": timestamp,
  "shift_length": 1,
  "shifts": [1, 2, 3, 4]
}
```

- **columns**: The number of columns (time units) this cell should take up.
- **open_on_left**: Whether this cell should be *open* on the left since it
  extends into the previous day.
- **open_on_right**: Whether this cell should be *open* on the right since it
  extends into the next day.
- **start_time**: timestamp for when this set of shifts start.
- **end_time**: timestamp for when this set of shifts end.
- **shift_length**: number of time units long this shift is.
- **shifts**: Array of shift id's that this cell represents.
