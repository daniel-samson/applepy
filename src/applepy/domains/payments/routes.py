"""Payment routes with composite key support."""

from flask import Blueprint, Response, jsonify, request

from applepy.session import get_session

from .schemas import PaymentCreate, PaymentRecord
from .service import PaymentService


class PaymentRoutes:
    """Routes for payments with composite primary key.

    Endpoints:
    - GET /payments - List all payments
    - GET /payments/<customer_number>/<check_number> - Get by composite key
    - GET /customers/<customer_number>/payments - Get all payments for customer
    - POST /payments - Create new payment
    - PUT /payments/<customer_number>/<check_number> - Update payment
    - DELETE /payments/<customer_number>/<check_number> - Delete payment
    """

    path = "/payments"

    @classmethod
    def register(cls, app: Blueprint) -> None:
        """Register routes with Flask app."""
        app.add_url_rule(
            cls.path,
            f"{cls.path}_list",
            cls.list_all,
            methods=["GET"],
        )
        app.add_url_rule(
            f"{cls.path}/<int:customer_number>/<check_number>",
            f"{cls.path}_get",
            cls.get,
            methods=["GET"],
        )
        app.add_url_rule(
            "/customers/<int:customer_number>/payments",
            f"{cls.path}_by_customer",
            cls.get_by_customer,
            methods=["GET"],
        )
        app.add_url_rule(
            cls.path,
            f"{cls.path}_create",
            cls.create,
            methods=["POST"],
        )
        app.add_url_rule(
            f"{cls.path}/<int:customer_number>/<check_number>",
            f"{cls.path}_update",
            cls.update,
            methods=["PUT"],
        )
        app.add_url_rule(
            f"{cls.path}/<int:customer_number>/<check_number>",
            f"{cls.path}_delete",
            cls.delete,
            methods=["DELETE"],
        )

    @staticmethod
    def list_all() -> Response:
        """List all payments."""
        with get_session() as session:
            service = PaymentService(session)
            records = service.all()
            return jsonify([r.model_dump() for r in records])

    @staticmethod
    def get(customer_number: int, check_number: str) -> Response:
        """Get payment by composite key."""
        with get_session() as session:
            service = PaymentService(session)
            record = service.get(customer_number, check_number)
            return jsonify(record.model_dump())

    @staticmethod
    def get_by_customer(customer_number: int) -> Response:
        """Get all payments for a customer."""
        with get_session() as session:
            service = PaymentService(session)
            records = service.get_by_customer(customer_number)
            return jsonify([r.model_dump() for r in records])

    @staticmethod
    def create() -> tuple[Response, int]:
        """Create new payment."""
        data = PaymentCreate(**request.get_json())
        with get_session() as session:
            service = PaymentService(session)
            record = service.create(data)
            session.commit()
            return jsonify(record.model_dump()), 201

    @staticmethod
    def update(customer_number: int, check_number: str) -> Response:
        """Update payment."""
        json_data = request.get_json()
        json_data["customer_number"] = customer_number
        json_data["check_number"] = check_number
        data = PaymentRecord(**json_data)
        with get_session() as session:
            service = PaymentService(session)
            record = service.update(data)
            session.commit()
            return jsonify(record.model_dump())

    @staticmethod
    def delete(customer_number: int, check_number: str) -> tuple[Response, int]:
        """Delete payment."""
        with get_session() as session:
            service = PaymentService(session)
            service.delete(customer_number, check_number)
            session.commit()
            return jsonify({"message": "Deleted"}), 200
