from routes.route_property import property_bp
from routes.route_unit import unit_bp
from routes.route_lease import lease_bp
from routes.route_tenant import tenant_bp
from routes.route_analytics import analytics_bp

def register_routes(app):
    app.register_blueprint(property_bp, url_prefix='/properties')
    app.register_blueprint(unit_bp, url_prefix='/units')
    app.register_blueprint(lease_bp, url_prefix='/leases')
    app.register_blueprint(tenant_bp, url_prefix='/tenants')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
