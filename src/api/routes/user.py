from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Dict, Any
from .database_manager import datbase_manager

user_blueprint = Blueprint("user", __name__, url_prefix="/user")

@user_blueprint.route("/student/new", methods=["POST"])
def new_student():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No input data provided"}), 400
  
  nome = data.get("nome")
  email = data.get("email")
  tel = data.get("tel")
  second_tel = data.get("second_tel")
  ra = data.get("ra")
  password = data.get("password")

  if not all([nome, email, tel, ra, password]):
    return jsonify({"error": "Missing required fields (nome, email, tel, ra, password)"}), 400

  try:
    hashed_password = generate_password_hash(password)
    
    _, cursor = datbase_manager.get_connection()
    
    cursor.execute(
      "INSERT INTO users (password, nome, email, tel, second_tel) VALUES (%s, %s, %s, %s, %s)",
      (hashed_password, nome, email, tel, second_tel)
    )
    user_id = cursor.lastrowid

    cursor.execute(
      "INSERT INTO students (ra, user_id) VALUES (%s, %s)",
      (ra, user_id)
    )

    datbase_manager._execute_commit()
    return jsonify({"message": "Student created successfully", "user_id": user_id, "ra": ra}), 201

  except Exception as e:
    datbase_manager._excute_rollback()
    return jsonify({"error": str(e)}), 500

@user_blueprint.route("/student/login", methods=["POST"])
def login_student():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No input data provided"}), 400

  email = data.get("email")
  password = data.get("password")

  if not all([email, password]):
    return jsonify({"error": "Missing email or password"}), 400

  try:
    results = datbase_manager._execute_select(
      table="users u JOIN students s ON u.id = s.user_id",
      fields=["u.id", "u.password", "u.nome", "u.email", "s.ra"],
      where_query="u.email = %s",
      values=[email]
    )

    if results:
      student = results[0]
      if check_password_hash(student["password"], password):
        del student["password"]
        return jsonify({"message": "Login successful", "student": student}), 200
      
    return jsonify({"error": "Invalid email or password"}), 401

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@user_blueprint.route("/student/get/<int:id>", methods=["GET"])
def get_student(id):
  try:
    results = datbase_manager._execute_select(
      table="users u JOIN students s ON u.id = s.user_id",
      fields=["u.id", "u.nome", "u.email", "u.tel", "u.second_tel", "s.ra"],
      where_query="u.id = %s",
      values=[id]
    )

    if results:
      return jsonify(results[0]), 200
    else:
      return jsonify({"error": "Student not found"}), 404

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@user_blueprint.route("/employee/new", methods=["POST"])
def new_employee():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No input data provided"}), 400

  nome = data.get("nome")
  email = data.get("email")
  tel = data.get("tel")
  second_tel = data.get("second_tel")
  cpf = data.get("cpf")
  job_role = data.get("job_role") # 'teacher' ou 'library'
  password = data.get("password")

  if not all([nome, email, tel, cpf, job_role, password]):
    return jsonify({"error": "Missing required fields (nome, email, tel, cpf, job_role, password)"}), 400

  try:
    hashed_password = generate_password_hash(password)

    _, cursor = datbase_manager.get_connection()
    
    # 1. Insere o usuário base (incluindo a senha com hash)
    cursor.execute(
      "INSERT INTO users (password, nome, email, tel, second_tel) VALUES (%s, %s, %s, %s, %s)",
      (hashed_password, nome, email, tel, second_tel)
    )
    func_id = cursor.lastrowid

    # 2. Insere o funcionário vinculado ao usuário
    cursor.execute(
      "INSERT INTO employees (cpf, func_id, job_role) VALUES (%s, %s, %s)",
      (cpf, func_id, job_role)
    )

    datbase_manager._execute_commit()
    return jsonify({"message": "Employee created successfully", "func_id": func_id, "cpf": cpf}), 201

  except Exception as e:
    datbase_manager._excute_rollback()
    return jsonify({"error": str(e)}), 500

@user_blueprint.route("/employee/login", methods=["POST"])
def login_employee():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No input data provided"}), 400

  email = data.get("email")
  password = data.get("password")

  if not all([email, password]):
    return jsonify({"error": "Missing email or password"}), 400

  try:
    # Buscamos o funcionário pelo email, trazendo a senha armazenada
    results = datbase_manager._execute_select(
      table="users u JOIN employees e ON u.id = e.func_id",
      fields=["u.id", "u.password", "u.nome", "u.email", "e.cpf", "e.job_role"],
      where_query="u.email = %s",
      values=[email]
    )

    if results:
      employee = results[0]
      if check_password_hash(employee["password"], password):
        del employee["password"]
        return jsonify({"message": "Login successful", "employee": employee}), 200
      
    return jsonify({"error": "Invalid email or password"}), 401

  except Exception as e:
    return jsonify({"error": str(e)}), 500

@user_blueprint.route("/employee/get/<int:id>", methods=["GET"])
def get_employee(id):
  try:
    results = datbase_manager._execute_select(
      table="users u JOIN employees e ON u.id = e.func_id",
      fields=["u.id", "u.nome", "u.email", "u.tel", "u.second_tel", "e.cpf", "e.job_role"],
      where_query="u.id = %s",
      values=[id]
    )

    if results:
      return jsonify(results[0]), 200
    else:
      return jsonify({"error": "Employee not found"}), 404

  except Exception as e:
    return jsonify({"error": str(e)}), 500