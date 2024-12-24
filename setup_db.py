import csv
from db import db
from db_models import Property, Unit, Lease, Tenant
from common import convert_to_date


# Define file paths for CSVs
FILES_PATH = "files/"
PROPERTIES_CSV = FILES_PATH + "properties.csv"
UNITS_CSV = FILES_PATH + "units.csv"
LEASES_CSV = FILES_PATH + "leases.csv"


def populate_properties():
    with open(PROPERTIES_CSV, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            property_entry = Property(
                property_id=row["property_id"],
                property_name=row["property_name"],
                address=row["address"],
            )
            db.session.add(property_entry)


def populate_units():
    with open(UNITS_CSV, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            unit_entry = Unit(
                unit_id=row["unit_id"],
                property_id=row["property_id"],
                unit_number=row["unit_number"],
                size=row["size"],
                type=row["type"],
            )
            db.session.add(unit_entry)


def populate_leases():
    with open(LEASES_CSV, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lease_entry = Lease(
                lease_id=row["lease_id"],
                unit_id=row["unit_id"],
                tenant_id=row["tenant_id"],
                start_date=convert_to_date(row["start_date"]),
                end_date=convert_to_date(row["end_date"]),
            )
            db.session.add(lease_entry)


def populate_tenants():
    tenant_ids = set()
    with open(LEASES_CSV, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tenant_ids.add(row["tenant_id"])

    for tenant_id in tenant_ids:
        tenant_entry = Tenant(tenant_id=tenant_id)
        db.session.add(tenant_entry)


def initialize_database():
    db.drop_all()
    db.create_all()
    populate_properties()
    populate_units()
    populate_leases()
    populate_tenants()
    db.session.commit()
    print("Database initialized and populated successfully!")
