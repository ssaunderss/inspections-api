# Health Inspection Flask API

## Setup 

### Postgres Backend

This project uses a postgres backend defined in `docker-compose.yaml`. To get this up and running, run `docker-compose --up` from the root of the `inspections-api` directory.

If you have to restart the postgres container for any reason use `docker-compose down --volumes` so that it gets rid of the postgres cache and doesn't create any problems on restart.

### Pipenv Environment

This project uses pipenv to manage dependencies. You can run `pip install pipenv` from your regular Python setup. From the project root, you can then run `pipenv install` to install dependencies.

### Starting the Flask Server

You can enter a virtualenv with the dependencies installed in the previous step by running `pipenv shell`.

**Before you can start the server**, you first need to run the db migrations which can be performed by `flask db upgrade`.

Once the migrations are up and running, run `flask run` to start the server.

## API Explanation

### Important pieces of code
- `app/models.py`: The models code is responsible for adding all new tables to the db (via flask migrations), and the formatting / parsing of objects going / coming. The db is broken into three seperate tables `restaurant`, `inspection`, and `violation`. The `restaurant` table records the restaurant portion of an inspection payload. The `violation` table records each violation listed in an inspection payload by its `violation_id` and also records the `inspection_id` as a foreign key so violations can be retrieved by inspection. The `inspection` table records the top-level body of the inspection - i.e. `inspection_id`, `score`, etc., it also records `restaurant_id` as a foreign key, so restaurant can be retrieved off of an inspection id. 
- `validations.py`: responsible for handling all of the validation logic for incoming inspection payloads. More on this in the endpoints section below.
- `app/api/inspections.py`: holds the blueprint/logic for the inspection endpoints

### Endpoints

#### POST /health-inspections/api/v1/inspections

- The payload is first loaded into a validation schema, which uses the `marshmallow` library. All of the validation logic can be found in `app/validations.py`. A validation class was created for each component of the payload (inspection, restaurant, violations), and used the db schema constraints for each respective class (found in `app/models.py`), along with a few custom validations that required a bit more complexity:
    - `restaurant.state`: needs to be an abbreviated US state (2 chars)
    - `inspection.inspection_date`: date has to be less than or equal to today's date
    - `restaurant.street_address`: this is a pretty nuanced field to validate, but for now it is just using a regex pattern as validation on this field, however this is not a bulletproof solution - i.e. the invalid street address '3325 A' would pass because the pattern 101 W is valid. If this was a prod system, more time would be spent on the address validation by probably utilizing a third party API to validate these addresses.
- After validation, the validation object is passed along and stored in the db in three stages, one for each component (restaurant, inspection (body), and violations). They have to be stored in this order because of the object relationships between them in the db.
- After the changes are committed to the db, a 201 response is returned signalling a successful POST
- If the payload doesn't pass validation, a validation error will be returned, which includes `inspection_id` and field-level validation errors

### GET /health-inspections/api/v1/inspections/:id

- This endpoint receives an integer inspection id and returns a formatted inspection response include the inspection body, restauarant, and violations.
- This endpoint first grabs the inspection body by running a query, if it doesn't exist a 404 is returned. If the inspection does exist, the endpoint also grabs the corresponding restaurant and violations. Once the data is collected it's formatted into response and returned with a 200.

## Testing

The validation logic code is in `tests.py`, to run the code use `python3 tests.py` from within the `pipenv shell`.