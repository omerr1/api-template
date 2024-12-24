from flask import Blueprint, jsonify, request
from db_models import Property
from db import db
from pydantic_models import PropertySchema
from pydantic import ValidationError

property_bp = Blueprint("property", __name__)


@property_bp.route("/", methods=["GET"])
def get_properties():
    properties = Property.query.all()
    return jsonify(
        [
            {
                "property_id": p.property_id,
                "property_name": p.property_name,
                "address": p.address,
            }
            for p in properties
        ]
    )


@property_bp.route("/", methods=["POST"])
def create_property():
    try:
        data = PropertySchema(**request.json)
        new_property = Property(property_name=data.property_name, address=data.address)
        db.session.add(new_property)
        db.session.commit()
        return (
            jsonify(
                {
                    "property_id": new_property.property_id,
                    "property_name": new_property.property_name,
                    "address": new_property.address,
                }
            ),
            201,
        )
    except ValidationError as e:
        return jsonify(e.errors()), 400
