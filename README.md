# Idoven Backend Coding Challenge

* **Candidate:** Pablo Chinea <khertz@gmail.com>
* **Date:** March 2024

## Implementation

The challenge is implemented with Python 3.11 (but it will work from version 3.8 onwards), using FastAPI and 
SQLAlchemy. 

Fastapi-users has been used for user management, this library offers a multitude of features, but only those necessary 
to meet the requested use case have been integrated (login, logout and register). Since only an admin user can register 
new users through the API, a script is implemented to create administrator users.

For simplicity, an SQLite database is used, but since it is managed by SQLAlchemy it would be easily replaceable by 
another database. The Alembic migration tool has also been used to facilitate the possible incorporation of new 
functionalities.

### Assumptions

Since it is not specified what type of identifier is used by the ECGs, the type UUID is expected. It is specified that 
the ECG signal contains positive and negative numbers, I assume that it can also contain zero, in the event that the 
signal touches zero but does not cross it (which I do not know if it is possible or not) it is not counted, only it is 
counted when it crosses from positive to negative and vice versa.

## Deployment

The dependencies are listed in the `requirements.txt` file, so to test the project dependencies must be installed in 
the environment (e.g. virtualenv):

    $ pip install -r requirements.txt

The application is run locally using a Makefile command:

    $ make run

With this command, before starting the application, the database is initialized and an administrator user is created:

  * Username: `admin@example.com`
  * Password: `1234`

If necessary, new administrator users can be created with `create_super_user.py` script:

    $ python create_super_user.py <email> <password>

To test the API an example file is also provided (using UUID as ECG identification): [example.json](example.json)

## Testing

The test suite is implemented with pytest, it is also executed with a Makefile command:

    $ make run_tests

## Possible improvements

The data model is designed so that new insights can be added, so adding them to this model would already be available 
through the implemented endpoint. 

In this case, since the requested insight is a simple calculation, it is performed during the ECG loading. In the 
future, when there are more and more complex calculations, a deferred task should be used (using celery, for example).

As said before, for simplicity, user management integration is intentionally simple, to be used in production more 
functionalities would have to be integrated.