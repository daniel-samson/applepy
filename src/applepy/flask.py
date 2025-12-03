from flask import Blueprint

from applepy.domains.customers.routes import CustomerRoutes
from applepy.domains.employees.routes import EmployeeRoutes
from applepy.domains.offices.routes import OfficeRoutes
from applepy.domains.order_details.routes import OrderDetailRoutes
from applepy.domains.orders.routes import OrderRoutes
from applepy.domains.payments.routes import PaymentRoutes
from applepy.domains.product_lines.routes import ProductLineRoutes
from applepy.domains.products.routes import ProductRoutes
from applepy.factory import create_app
from applepy.responses import ApiResponse, FlaskApiResponse

app = create_app()

# Register domain route blueprints
app.register_blueprint(OfficeRoutes().blueprint)
app.register_blueprint(EmployeeRoutes().blueprint)
app.register_blueprint(CustomerRoutes().blueprint)
app.register_blueprint(ProductLineRoutes().blueprint)
app.register_blueprint(ProductRoutes().blueprint)
app.register_blueprint(OrderRoutes().blueprint)

# Register routes with composite keys (custom registration)
order_details_bp = Blueprint("order_details", __name__)
OrderDetailRoutes.register(order_details_bp)
app.register_blueprint(order_details_bp)

payments_bp = Blueprint("payments", __name__)
PaymentRoutes.register(payments_bp)
app.register_blueprint(payments_bp)


@app.route("/", methods=["GET"])
def hello_world() -> FlaskApiResponse:
    response: ApiResponse[None] = ApiResponse(message="Hello, World!")
    return response.model_dump(), 200
