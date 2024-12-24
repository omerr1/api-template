from flask import Blueprint, jsonify, request
from db_models import Lease
from db import db
from pydantic_models import LeaseSchema
from pydantic import ValidationError
from datetime import datetime, timedelta

lease_bp = Blueprint("lease", __name__)


@lease_bp.route("/", methods=["GET"])
def get_leases():
    leases = Lease.query.all()
    return jsonify(
        [
            {
                "lease_id": l.lease_id,
                "unit_id": l.unit_id,
                "tenant_id": l.tenant_id,
                "start_date": l.start_date.strftime("%Y-%m-%d"),
                "end_date": l.end_date.strftime("%Y-%m-%d"),
            }
            for l in leases
        ]
    )


@lease_bp.route("/", methods=["POST"])
def create_lease():
    try:
        data = LeaseSchema(**request.json)
        new_lease = Lease(
            unit_id=data.unit_id,
            tenant_id=data.tenant_id,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        db.session.add(new_lease)
        db.session.commit()
        return (
            jsonify(
                {
                    "lease_id": new_lease.lease_id,
                    "unit_id": new_lease.unit_id,
                    "tenant_id": new_lease.tenant_id,
                    "start_date": new_lease.start_date.strftime("%Y-%m-%d"),
                    "end_date": new_lease.end_date.strftime("%Y-%m-%d"),
                }
            ),
            201,
        )
    except ValidationError as e:
        return jsonify(e.errors()), 400


@lease_bp.route("/ending-soon", methods=["GET"])
def get_leases_ending_soon():
    # Default days to 30 if not provided
    days = int(request.args.get("days", 30))

    if days <= 0:
        return jsonify({"error": "Days parameter must be greater than 0"}), 400

    now = datetime.now()
    end_date = now + timedelta(days=days)

    # Query for leases ending within the range
    leases = Lease.query.filter(Lease.end_date.between(now, end_date)).all()

    return jsonify(
        [
            {
                "lease_id": l.lease_id,
                "unit_id": l.unit_id,
                "tenant_id": l.tenant_id,
                "start_date": l.start_date.strftime("%Y-%m-%d"),
                "end_date": l.end_date.strftime("%Y-%m-%d"),
            }
            for l in leases
        ]
    )
