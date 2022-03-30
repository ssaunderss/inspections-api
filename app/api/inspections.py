from flask import request, jsonify, request, url_for

from app import db
from app.api import bp 
from app.models import Restaurant, Inspection, Violation
from app.validations import *

@bp.route('/health-inspections/api/v1/info', methods=['GET'])
def info():
    """List of routes for this API"""
    info = {
        'store inspection' : 'POST /inspections/api/v1/inspections',
        'retrieve inspection' : 'GET /inspections/api/v1/inspections/<inspection_id>',
        'retrieve restaurant inspections' : 'GET /inspections/api/v1/restaurants/<restaurant_id>'
    }
    return jsonify(info)

@bp.route("/health-inspections/api/v1/inspections", methods=["POST"])
def validate_and_store():
    request_body = request.json
    inspection_schema = InspectionSchema()
    try:
        inspection_result = inspection_schema.load(request_body)
    except ValidationError as e:
        error_response = {
            'inspection_id': request_body['inspection_id'],
            'errors': e.messages
        }
        return jsonify(error_response), 400
    
    # Insert restaurant only if it doesn't already exist in restaurant table
    if not Restaurant.query.filter_by(restaurant_id=inspection_result['restaurant']['restaurant_id']):
        restaurant = Restaurant()
        restaurant.from_dict(inspection_result['restaurant'])
        db.session.add(restaurant)

    # Insert inspection
    inspection = Inspection()
    inspection.from_dict(inspection_result)
    db.session.add(inspection)

    # Insert violation(s)
    for violation in inspection_result['violations']:
        tmp_violation = Violation()
        tmp_violation.from_dict(violation)
        tmp_violation.inspection_id = inspection_result['inspection_id']
        db.session.add(tmp_violation)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify(e), 400
    
    response = jsonify(inspection_result)
    response.status = 201
    response.headers['Location'] = url_for('api.get_inspection', 
        inspection_id=inspection_result['inspection_id'])

    return response

@bp.route("/health-inspectionss/api/v1/inspections/<int:id>", methods=["GET"])
def get_inspection(id):

    inspection = Inspection.query.get_or_404(id)
    restaurant = Restaurant.query.get(inspection.restaurant_id)
    violations = Violation.query.filter_by(inspection_id=id).all()
    
    inspection = inspection.to_dict()
    inspection['restaurant'] = restaurant.to_dict()
    inspection['violations'] = [v.to_dict() for v in violations]

    response = jsonify(inspection)
    return response, 200
