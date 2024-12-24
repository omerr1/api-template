from flask import Blueprint, jsonify, request
from db_models import Tenant
from db import db
from pydantic_models import TenantSchema
from pydantic import ValidationError

tenant_bp = Blueprint('tenant', __name__)

# Get all tenants
@tenant_bp.route('/', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([{"tenant_id": t.tenant_id} for t in tenants])

# Create a new tenant
@tenant_bp.route('/', methods=['POST'])
def create_tenant():
    try:
        data = TenantSchema(**request.json)
        new_tenant = Tenant(tenant_id=data.tenant_id)
        db.session.add(new_tenant)
        db.session.commit()
        return jsonify({"tenant_id": new_tenant.tenant_id}), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400
