from typing import Any

from flask import Flask, request
from sqlalchemy.orm.session import Session

from applepy.db import Base, db, engine
from applepy.domains.offices.schemas import OfficeCreate, OfficeRecord
from applepy.domains.offices.service import OfficeService
from applepy.env import DATABASE_URL
from applepy.exceptions import NotFoundException
from applepy.responses import ApiResponse, ListResponse

app = Flask("applepy")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

# Create tables immediately on module load
Base.metadata.create_all(engine)


@app.route("/", methods=["GET"])
def hello_world() -> tuple[dict[str, Any], int]:
    response: ApiResponse[None] = ApiResponse(message="Hello, World!")
    return response.model_dump(), 200


@app.route("/offices", methods=["GET"])
def get_offices() -> tuple[dict[str, Any], int]:
    session: Session = db.session()
    try:
        office_service = OfficeService(session)
        offices = office_service.get_all_offices()
        list_response: ListResponse[OfficeRecord] = ListResponse(
            items=list(offices), count=len(offices)
        )
        response: ApiResponse[ListResponse[OfficeRecord]] = ApiResponse(
            data=list_response
        )
        return response.model_dump(), 200
    except Exception as e:
        error_response: ApiResponse[None] = ApiResponse(error=str(e))
        return error_response.model_dump(), 500
    finally:
        session.close()


@app.route("/offices/<office_code>", methods=["GET"])
def get_office(office_code: str) -> tuple[dict[str, Any], int]:
    session: Session = db.session()
    try:
        office_service = OfficeService(session)
        office = office_service.get_office_by_id(office_code)
        response: ApiResponse[OfficeRecord] = ApiResponse(data=office)
        return response.model_dump(), 200
    except NotFoundException as e:
        error_response: ApiResponse[None] = ApiResponse(error=str(e))
        return error_response.model_dump(), 404
    except Exception as e:
        error_response = ApiResponse(error=str(e))
        return error_response.model_dump(), 500
    finally:
        session.close()


@app.route("/offices", methods=["POST"])
def create_office() -> tuple[dict[str, Any], int]:
    try:
        data = request.get_json()
        if not data:
            error_response: ApiResponse[None] = ApiResponse(
                error="No JSON data provided"
            )
            return error_response.model_dump(), 400
        office = OfficeCreate(**data)
        session: Session = db.session()
        try:
            office_service = OfficeService(session)
            created_office = office_service.create_office(office)
            session.commit()
            response: ApiResponse[OfficeRecord] = ApiResponse(data=created_office)
            return response.model_dump(), 201
        finally:
            session.close()
    except Exception as e:
        error_response = ApiResponse(error=str(e))
        return error_response.model_dump(), 500


@app.route("/offices/<office_code>", methods=["PUT"])
def update_office(office_code: str) -> tuple[dict[str, Any], int]:
    try:
        data = request.get_json()
        if not data:
            error_response: ApiResponse[None] = ApiResponse(
                error="No JSON data provided"
            )
            return error_response.model_dump(), 400
        office = OfficeRecord(**data)
        # Validate that office_code in URL matches office_code in body
        if office.office_code != office_code:
            error_response = ApiResponse(
                error="office_code in URL must match office_code in request body"
            )
            return error_response.model_dump(), 400
        session: Session = db.session()
        try:
            office_service = OfficeService(session)
            updated_office = office_service.update_office(office)
            session.commit()
            response: ApiResponse[OfficeRecord] = ApiResponse(data=updated_office)
            return response.model_dump(), 200
        finally:
            session.close()
    except NotFoundException as e:
        error_response = ApiResponse(error=str(e))
        return error_response.model_dump(), 404
    except Exception as e:
        error_response_2: ApiResponse[None] = ApiResponse(error=str(e))
        return error_response_2.model_dump(), 500


@app.route("/offices/<office_code>", methods=["DELETE"])
def delete_office(office_code: str) -> tuple[dict[str, Any], int]:
    try:
        session: Session = db.session()
        try:
            office_service = OfficeService(session)
            office_service.delete_office_by_id(office_code)
            session.commit()
            response: ApiResponse[None] = ApiResponse(
                message="Office deleted successfully"
            )
            return response.model_dump(), 204
        finally:
            session.close()
    except NotFoundException as e:
        error_response: ApiResponse[None] = ApiResponse(error=str(e))
        return error_response.model_dump(), 404
    except Exception as e:
        error_response = ApiResponse(error=str(e))
        return error_response.model_dump(), 500
