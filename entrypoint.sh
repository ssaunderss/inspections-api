#!/bin/bash

# initialize the db
flask db init

# run all of the migrations
flask db upgrade

# start the flask app
pipenv shell
python3 -m flask run --host:0.0.0.0