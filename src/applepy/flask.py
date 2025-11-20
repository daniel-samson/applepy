from applepy.factory import create_app
from applepy.responses import ApiResponse, FlaskApiResponse
from applepy.routes.offices import OfficeRoutes

app = create_app()

# Register CRUD route blueprints
office_routes = OfficeRoutes()
app.register_blueprint(office_routes.blueprint)


@app.route("/", methods=["GET"])
def hello_world() -> FlaskApiResponse:
    response: ApiResponse[None] = ApiResponse(message="Hello, World!")
    return response.model_dump(), 200
