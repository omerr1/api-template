from flask import Blueprint, jsonify, request
from db_models import Unit
from db import db
from pydantic_models import UnitSchema
from pydantic import ValidationError

unit_bp = Blueprint('unit', __name__)

@unit_bp.route('/', methods=['GET'])
def get_units():
    units = Unit.query.all()
    return jsonify([
        {
            "unit_id": u.unit_id,
            "property_id": u.property_id,
            "unit_number": u.unit_number,
            "size": u.size,
            "type": u.type
        } for u in units
    ])

@unit_bp.route('/', methods=['POST'])
def create_unit():
    try:
        data = UnitSchema(**request.json)
        new_unit = Unit(property_id=data.property_id, unit_number=data.unit_number, size=data.size, type=data.type)
        db.session.add(new_unit)
        db.session.commit()
        return jsonify({
            "unit_id": new_unit.unit_id,
            "property_id": new_unit.property_id,
            "unit_number": new_unit.unit_number,
            "size": new_unit.size,
            "type": new_unit.type
        }), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
