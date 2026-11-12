from mysql.connector import Error
from db import DatabaseManager, Env

TABLES_SCHEMA = {
    "users": [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "nome VARCHAR(255) NOT NULL",
        "email VARCHAR(255) UNIQUE NOT NULL",
        "tel VARCHAR(20) UNIQUE NOT NULL",
        "second_tel VARCHAR(20)"
    ],
    "students": [
        "ra VARCHAR(50) PRIMARY KEY",
        "user_id INT NOT NULL",
        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE"
    ],
    "employees": [
        "cpf VARCHAR(14) PRIMARY KEY",
        "func_id INT NOT NULL",
        "job_role ENUM('teacher', 'library')",
        "FOREIGN KEY (func_id) REFERENCES users(id) ON DELETE CASCADE"
    ],
    "series": [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "name VARCHAR(255) NOT NULL",
        "description VARCHAR(255) NOT NULL"
    ],
    "books": [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "img VARCHAR(255)",
        "title VARCHAR(255) NOT NULL",
        "code VARCHAR(100) UNIQUE NOT NULL",
        "page_count INT",
        "synopsis TEXT",
        "serie_id INT",
        "category ENUM('horror', 'adventure', 'mystery', 'si-fi', 'romance', 'action', 'drama')",
        "FOREIGN KEY (serie_id) REFERENCES series(id) ON DELETE SET NULL"
    ],
    "book_rental_info": [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "rental_date DATE NOT NULL",
        "rental_days INT NOT NULL",
        "user_id INT NOT NULL",
        "book_id INT NOT NULL",
        "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE",
        "FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE"
    ],
    "authors": [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "name VARCHAR(255) NOT NULL",
        "mini_bio TEXT",
        "img VARCHAR(255)"
    ],
    "authorXbook": [
        "author_id INT NOT NULL",
        "book_id INT NOT NULL",
        "PRIMARY KEY (author_id, book_id)",
        "FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE",
        "FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE"
    ],
    "authorXserie": [
        "author_id INT NOT NULL",
        "serie_id INT NOT NULL",
        "PRIMARY KEY (author_id, serie_id)",
        "FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE",
        "FOREIGN KEY (serie_id) REFERENCES series(id) ON DELETE CASCADE"
    ],
    "lost_items": [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "img VARCHAR(255)",
        "date_of_acquisition DATE NOT NULL",
        "title VARCHAR(255) NOT NULL",
        "description TEXT",
        "type ENUM('clothes', 'electronic', 'school_material', 'other')"
    ]
}

def initialization_tables():
    try:
        database_commands_manager = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)
        
        print("Conectando e verificando a estrutura do banco de dados...")

        for table_name, fields in TABLES_SCHEMA.items():
            database_commands_manager._create_if_not_exist_table(table_name, fields)
            database_commands_manager._execute_commit()
            database_commands_manager.close_current_connection()
            print(f"-> Tabela '{table_name}' verificada/criada.")

        print("\nTodas as tabelas foram verificadas e estruturadas com sucesso!")

    except Error as e:
        print(f"Erro ao operar no MySQL: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    initialization_tables()
