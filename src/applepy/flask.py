from typing import Any, Union

from flask import Flask, request
from sqlalchemy.orm.session import Session

from applepy.db import Base, db, engine
from applepy.domains.offices.schemas import OfficeCreate, OfficeRecord
from applepy.domains.offices.service import OfficeService
from applepy.env import DATABASE_URL
from applepy.exceptions import NotFoundException

app = Flask("applepy")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

# Create tables immediately on module load
Base.metadata.create_all(engine)


@app.route("/", methods=["GET"])
def hello_world() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.route("/offices", methods=["GET"])
def get_offices() -> Union[tuple[dict[str, Any], int], dict[str, list[dict[str, Any]]]]:
    session: Session = db.session()
    try:
        office_service = OfficeService(session)
        offices = office_service.get_all_offices()
        return {"offices": [office.model_dump() for office in offices]}
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        session.close()


@app.route("/offices/<office_code>", methods=["GET"])
def get_office(
    office_code: str,
) -> Union[tuple[dict[str, Any], int], dict[str, dict[str, Any]]]:
    session: Session = db.session()
    try:
        office_service = OfficeService(session)
        office = office_service.get_office_by_id(office_code)
        return {"office": office.model_dump()}
    except NotFoundException as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        session.close()


@app.route("/offices", methods=["POST"])
def create_office() -> Union[tuple[dict[str, Any], int], dict[str, dict[str, Any]]]:
    try:
        data = request.get_json()
        if not data:
            return {"error": "No JSON data provided"}, 400
        office = OfficeCreate(**data)
        session: Session = db.session()
        try:
            office_service = OfficeService(session)
            created_office = office_service.create_office(office)
            session.commit()
            return {"office": created_office.model_dump()}
        finally:
            session.close()
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/offices/<office_code>", methods=["PUT"])
def update_office(
    office_code: str,
) -> Union[tuple[dict[str, Any], int], dict[str, dict[str, Any]]]:
    try:
        data = request.get_json()
        if not data:
            return {"error": "No JSON data provided"}, 400
        office = OfficeRecord(**data)
        session: Session = db.session()
        try:
            office_service = OfficeService(session)
            updated_office = office_service.update_office(office)
            session.commit()
            return {"office": updated_office.model_dump()}
        finally:
            session.close()
    except NotFoundException as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/offices/<office_code>", methods=["DELETE"])
def delete_office(
    office_code: str,
) -> Union[tuple[dict[str, Any], int], dict[str, str]]:
    try:
        session: Session = db.session()
        try:
            office_service = OfficeService(session)
            office_service.delete_office_by_id(office_code)
            session.commit()
            return {"message": "Office deleted"}
        finally:
            session.close()
    except NotFoundException as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 500
