from flask import Blueprint, jsonify, request
from typing import List, Dict, Any
from .database_manager import datbase_manager

serie_blueprint = Blueprint("serie", __name__, url_prefix="/serie")

@serie_blueprint.route("/new", methods=["POST"])
def new_serie():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    name = data.get("name")
    description = data.get("description")

    if not all([name, description]):
        return jsonify({"error": "Missing required fields (name, description)"}), 400

    try:
        datbase_manager._execute_insert(
            table="series",
            fields=["name", "description"],
            values=[name, description]
        )
        datbase_manager._execute_commit()
        
        return jsonify({"message": "Serie created successfully", "name": name}), 201

    except Exception as e:
        datbase_manager._excute_rollback()
        return jsonify({"error": str(e)}), 500

@serie_blueprint.route("/<int:id>", methods=["GET"])
def get_serie(id):
    try:
        results = datbase_manager._execute_select(
            table="series",
            fields=["id", "name", "description"],
            where_query="id = %s",
            values=[id]
        )

        if results:
            return jsonify(results[0]), 200
        else:
            return jsonify({"error": "Serie not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@serie_blueprint.route("/page/<int:page>", methods=["GET"])
def get_series_by_page(page):
    try:
        if page < 1:
            return jsonify({"error": "Page number must be 1 or greater"}), 400

        per_page = 10
        offset = (page - 1) * per_page

        extra_query = f"LIMIT {per_page} OFFSET {offset}"

        series = datbase_manager._execute_select(
            table="series",
            fields=["id", "name", "description"],
            extra_query=extra_query
        )

        return jsonify({"page": page, "per_page": per_page, "series": series}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500