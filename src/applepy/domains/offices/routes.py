"""Office CRUD routes."""

from applepy.routes.base import CrudRoutes

from .schemas import OfficeCreate, OfficeRecord
from .service import OfficeService


class OfficeRoutes(CrudRoutes[OfficeCreate, OfficeRecord, str]):
    """CRUD routes for offices.

    Automatically generates:
    - GET /offices - List all offices
    - GET /offices/<office_code> - Get office by code
    - POST /offices - Create new office
    - PUT /offices/<office_code> - Update office
    - DELETE /offices/<office_code> - Delete office
    """

    path = "/offices"
    service_class = OfficeService
    create_schema = OfficeCreate
    record_schema = OfficeRecord
    id_param_name = "office_code"
