from flask import Blueprint, jsonify
from db_models import Lease
from datetime import datetime, timedelta, timezone, date

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/top-vacancies", methods=["GET"])
def get_top_vacancies():
    one_year_ago = date.today() - timedelta(days=365)

    # Get all leases that ended within the last year
    leases = (
        Lease.query.filter(Lease.end_date >= one_year_ago)
        .order_by(Lease.unit_id, Lease.end_date)
        .all()
    )

    # Calculate vacancies per unit
    unit_vacancies = {}
    for i, lease in enumerate(leases):
        unit_id = lease.unit_id
        if unit_id not in unit_vacancies:
            unit_vacancies[unit_id] = []

        # If there's a next lease for the same unit, calculate the gap
        if i + 1 < len(leases) and leases[i + 1].unit_id == unit_id:
            next_lease = leases[i + 1]
            vacancy_days = (next_lease.start_date - lease.end_date).days
        else:
            # If no subsequent lease, calculate gap to current date
            vacancy_days = (date.today() - lease.end_date).days

        if vacancy_days > 30:
            unit_vacancies[unit_id].append(vacancy_days)

    # Filter out units with no valid vacancies
    filtered_vacancies = {
        unit_id: vacancies for unit_id, vacancies in unit_vacancies.items() if vacancies
    }

    # Get the top 5 units by longest vacancy
    top_vacancies = sorted(
        [
            (unit_id, max(vacancies))
            for unit_id, vacancies in filtered_vacancies.items()
        ],
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    # Format response
    result = [
        {"unit_id": unit_id, "vacancy_days": days} for unit_id, days in top_vacancies
    ]

    return jsonify(result)
