from flask import Blueprint, jsonify, request
from typing import List, Dict, Any
from .database_manager import datbase_manager

book_blueprint = Blueprint("book", __name__, url_prefix="/book")

@book_blueprint.route("/new", methods=["POST"])
def new_book():
    try:
        data = request.get_json()
        
        required_fields = ["title", "code"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Campos obrigatórios ausentes: title, code"}), 400
            
        fields = ["img", "title", "code", "page_count", "synopsis", "serie_id", "category"]
        
        values = [data.get(field) for field in fields]
        
        datbase_manager._execute_insert("books", fields, values)
        datbase_manager._execute_commit()
        
        return jsonify({"message": "Livro cadastrado com sucesso!"}), 201
        
    except Exception as e:
        datbase_manager._excute_rollback()
        return jsonify({"error": f"Erro ao cadastrar livro: {str(e)}"}), 500
    finally:
        datbase_manager.close_current_connection()


@book_blueprint.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    try:
        fields = ["id", "img", "title", "code", "page_count", "synopsis", "serie_id", "category"]
        
        result = datbase_manager._execute_select(
            table="books",
            fields=fields,
            where_query="WHERE id = %s",
            values=[book_id]
        )
        
        if not result:
            return jsonify({"error": "Livro não encontrado"}), 404
        
        book_data = dict(zip(fields, result[0]))
        return jsonify(book_data), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar livro: {str(e)}"}), 500
    finally:
        datbase_manager.close_current_connection()


@book_blueprint.route("/search", methods=["GET"])
def search_book():
    try:
        title_query = request.args.get("title")
        category_query = request.args.get("category")
        
        fields = ["id", "img", "title", "code", "page_count", "synopsis", "serie_id", "category"]
        
        where_clauses = []
        values = []
        
        if title_query:
            where_clauses.append("title LIKE %s")
            values.append(f"%{title_query}%")
            
        if category_query:
            where_clauses.append("category = %s")
            values.append(category_query)
            
        where_query = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        results = datbase_manager._execute_select("books", fields, where_query, values)
        
        books_list = [dict(zip(fields, row)) for row in results]
        return jsonify(books_list), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao pesquisar livros: {str(e)}"}), 500
    finally:
        datbase_manager.close_current_connection()


@book_blueprint.route("/login", methods=["POST"])
def user_login():
    try:
        data = request.get_json()
        email = data.get("email")
        
        if not email:
            return jsonify({"error": "O campo email é obrigatório para o login"}), 400
            
        fields = ["id", "nome", "email"]
        result = datbase_manager._execute_select(
            table="users",
            fields=fields,
            where_query="WHERE email = %s",
            values=[email]
        )
        
        if not result:
            return jsonify({"error": "Usuário não encontrado"}), 401
            
        user_data = dict(zip(fields, result[0]))
        return jsonify({"message": "Login bem-sucedido!", "user": user_data}), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar login: {str(e)}"}), 500
    finally:
        datbase_manager.close_current_connection()
