from flask import Flask
from sqlalchemy.orm.session import Session

from applepy.db import db
from applepy.domains.offices.schemas import OfficeCreate, OfficeRecord
from applepy.domains.offices.service import OfficeService
from applepy.env import DATABASE_URL

app = Flask("applepy")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db.init_app(app)


@app.route("/", methods=["GET"])
def hello_world() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.route("/offices", methods=["GET"])
def get_offices() -> dict[str, list[dict[str, str]]]:
    session: Session = db.session()
    office_service = OfficeService(session)
    offices = office_service.get_all_offices()
    return {"offices": [office.model_dump() for office in offices]}


@app.route("/offices/<office_code>", methods=["GET"])
def get_office(office_code: str) -> dict[str, OfficeRecord]:
    session: Session = db.session()
    office_service = OfficeService(session)
    office = office_service.get_office_by_id(office_code)
    return {"office": office}


@app.route("/offices", methods=["POST"])
def create_office(office: OfficeCreate) -> dict[str, OfficeRecord]:
    session: Session = db.session()
    office_service = OfficeService(session)
    created_office = office_service.create_office(office)
    return {"office": created_office}


@app.route("/offices/<office_code>", methods=["PUT"])
def update_office(office_code: str, office: OfficeRecord) -> dict[str, OfficeRecord]:
    session: Session = db.session()
    office_service = OfficeService(session)
    updated_office = office_service.update_office(office)
    return {"office": updated_office}


@app.route("/offices/<office_code>", methods=["DELETE"])
def delete_office(office_code: str) -> dict[str, str]:
    session: Session = db.session()
    office_service = OfficeService(session)
    office_service.delete_office_by_id(office_code)
    return {"message": "Office deleted"}
