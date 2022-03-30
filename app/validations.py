from datetime import date
from marshmallow import Schema, fields, validate, ValidationError, validates

states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

# regex to match street address
street_address_regexp = "^([0-9]{2,10})([a-zA-z0-9/\\''(),\-\s]{2,255})$"

todays_date = date.today()

# Validator classes for Restaurants, notes: this is a nested class in InspectionSchema
class RestaurantDetailsSchema(Schema):
    cuisine_type = fields.Str(validate=validate.Length(min=2))

class RestaurantSchema(Schema):
    restaurant_id = fields.Int(validate=validate.Range(min=0), required=True)
    name = fields.Str(validate=validate.Length(min=3, max=256), required=True)
    city = fields.Str(validate=validate.Length(min=3, max=64), required=True)

    # state needs to be formatted as one of the acceptable short-format US states
    state = fields.Str(validate=validate.OneOf(states), required=True)

    # postal code has to be standard len 5 format, or empty
    postal_code = fields.Str(required=True)
    @validates("postal_code")
    def validate_postal_code(self, value):
        if len(value) not in [0,5]:
            raise ValidationError("postal_code must be length 5 or empty.")

    # street address needs to match regex defined at TOP
    street_address = fields.Str(validate=validate.Regexp(street_address_regexp), required=True)

    # non-required fields:
    details = fields.Nested(RestaurantDetailsSchema)

# Validator class for Violations *this is a nested class in InspectionSchema*
class ViolationsSchema(Schema):
    violation_id = fields.Int(validate=validate.Range(min=0), required=True)
    is_critical = fields.Bool(required=True)
    code = fields.Str(validate=validate.Length(min=1, max=32), required=True)
    description = fields.Str(validate=validate.Length(min=1, max=256), required=True)
    comments = fields.Str(validate=validate.Length(min=0), required=True)

    # non-required fields
    is_corrected_on_site = fields.Bool()
    is_repeat = fields.Bool()

# Validator class for Inspections
class InspectionSchema(Schema):
    inspection_id = fields.Int(validate=validate.Range(min=0), required=True)

    # Inspection date has to be LTE to today's date
    inspection_date = fields.Date(validate=lambda x: x <= todays_date, required=True)
    score = fields.Int(validate=validate.Range(min=0, max=100), required=True)
    comments = fields.Str(validate=validate.Length(min=0), required=True)

    # nested fields
    restaurant = fields.Nested(RestaurantSchema, required=True)
    violations = fields.List(fields.Nested(lambda: ViolationsSchema()), required=True)

    # non-required fields
    type = fields.Str(validate=validate.Length(min=1))
