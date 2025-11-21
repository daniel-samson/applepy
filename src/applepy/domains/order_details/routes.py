"""OrderDetail routes with composite key support."""

from flask import Blueprint, Response, jsonify, request

from applepy.session import get_session

from .schemas import OrderDetailCreate, OrderDetailRecord
from .service import OrderDetailService


class OrderDetailRoutes:
    """Routes for order details with composite primary key.

    Endpoints:
    - GET /order-details - List all order details
    - GET /order-details/<order_number>/<product_code> - Get by composite key
    - GET /orders/<order_number>/details - Get all details for an order
    - POST /order-details - Create new order detail
    - PUT /order-details/<order_number>/<product_code> - Update order detail
    - DELETE /order-details/<order_number>/<product_code> - Delete order detail
    """

    path = "/order-details"

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
            f"{cls.path}/<int:order_number>/<product_code>",
            f"{cls.path}_get",
            cls.get,
            methods=["GET"],
        )
        app.add_url_rule(
            "/orders/<int:order_number>/details",
            f"{cls.path}_by_order",
            cls.get_by_order,
            methods=["GET"],
        )
        app.add_url_rule(
            cls.path,
            f"{cls.path}_create",
            cls.create,
            methods=["POST"],
        )
        app.add_url_rule(
            f"{cls.path}/<int:order_number>/<product_code>",
            f"{cls.path}_update",
            cls.update,
            methods=["PUT"],
        )
        app.add_url_rule(
            f"{cls.path}/<int:order_number>/<product_code>",
            f"{cls.path}_delete",
            cls.delete,
            methods=["DELETE"],
        )

    @staticmethod
    def list_all() -> Response:
        """List all order details."""
        with get_session() as session:
            service = OrderDetailService(session)
            records = service.all()
            return jsonify([r.model_dump() for r in records])

    @staticmethod
    def get(order_number: int, product_code: str) -> Response:
        """Get order detail by composite key."""
        with get_session() as session:
            service = OrderDetailService(session)
            record = service.get(order_number, product_code)
            return jsonify(record.model_dump())

    @staticmethod
    def get_by_order(order_number: int) -> Response:
        """Get all order details for an order."""
        with get_session() as session:
            service = OrderDetailService(session)
            records = service.get_by_order(order_number)
            return jsonify([r.model_dump() for r in records])

    @staticmethod
    def create() -> tuple[Response, int]:
        """Create new order detail."""
        data = OrderDetailCreate(**request.get_json())
        with get_session() as session:
            service = OrderDetailService(session)
            record = service.create(data)
            session.commit()
            return jsonify(record.model_dump()), 201

    @staticmethod
    def update(order_number: int, product_code: str) -> Response:
        """Update order detail."""
        json_data = request.get_json()
        json_data["order_number"] = order_number
        json_data["product_code"] = product_code
        data = OrderDetailRecord(**json_data)
        with get_session() as session:
            service = OrderDetailService(session)
            record = service.update(data)
            session.commit()
            return jsonify(record.model_dump())

    @staticmethod
    def delete(order_number: int, product_code: str) -> tuple[Response, int]:
        """Delete order detail."""
        with get_session() as session:
            service = OrderDetailService(session)
            service.delete(order_number, product_code)
            session.commit()
            return jsonify({"message": "Deleted"}), 200
