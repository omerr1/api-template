from flask_sqlalchemy import SQLAlchemy
from db import db


class Property(db.Model):
    __tablename__ = "properties"
    property_id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    units = db.relationship("Unit", backref="property", lazy=True)


class Unit(db.Model):
    __tablename__ = "units"
    unit_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer, db.ForeignKey("properties.property_id"), nullable=False
    )
    unit_number = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    leases = db.relationship("Lease", backref="unit", lazy=True)


class Lease(db.Model):
    __tablename__ = "leases"
    lease_id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey("units.unit_id"), nullable=False)
    tenant_id = db.Column(
        db.Integer, db.ForeignKey("tenants.tenant_id"), nullable=False
    )
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class Tenant(db.Model):
    __tablename__ = "tenants"
    tenant_id = db.Column(db.Integer, primary_key=True)
