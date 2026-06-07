# DIS-project-group-47
Group 47 project for the Databases and Information Systems course 2026


## About the project
We have implemented a budget app.

The ER diagram can be found in /docs.

The RegEx can be found in the /register page, where we recognize an email on the form of [user]@group47.[domain] and [user]@gruppe47.[domain]. 

Views are in db/views.sql

Triggers are in db/triggers.sql


## Compilation and Running Instructions
Instructions to run:

Start a virtual environment in python
```shell
pip install -r requirements.txt
flask run
```

You can either use the default user with username: "user", and password: "password", or use the register page to create a user. Here you must use an email in the form [user]@group47.[domain] or [user]@gruppe47.[domain], with a password that is atleast 8 characters long and has a special character.