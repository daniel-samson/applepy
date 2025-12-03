from applepy.domains.customers.routes import CustomerRoutes
from applepy.domains.employees.routes import EmployeeRoutes
from applepy.domains.offices.routes import OfficeRoutes
from applepy.factory import create_app
from applepy.responses import ApiResponse, FlaskApiResponse

app = create_app()

# Register domain route blueprints
app.register_blueprint(OfficeRoutes().blueprint)
app.register_blueprint(EmployeeRoutes().blueprint)
app.register_blueprint(CustomerRoutes().blueprint)


@app.route("/", methods=["GET"])
def hello_world() -> FlaskApiResponse:
    response: ApiResponse[None] = ApiResponse(message="Hello, World!")
    return response.model_dump(), 200
