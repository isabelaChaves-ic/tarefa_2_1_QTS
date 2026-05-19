from flask import Blueprint, jsonify, request
from app.services import user_service

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(user_service.get_all_users())


@user_bp.route("/users/search", methods=["GET"])
def search_users():
    query = request.args.get("name", "")
    resultado = user_service.search_users_by_name(query)
    return jsonify(resultado)


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(user)


@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Nome é obrigatório"}), 400
    user = user_service.create_user(data["name"])
    if user is None:
        return jsonify({"error": "Usuário já existe"}), 409
    return jsonify(user), 201


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Nome é obrigatório"}), 400
    user = user_service.update_user(user_id, data["name"])
    if user is None:
        return jsonify({"error": "Usuário não encontrado ou nome já existe"}), 404
    return jsonify(user)


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = user_service.delete_user(user_id)
    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify({"message": "Usuário removido"})
