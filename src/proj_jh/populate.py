import datetime
from db import DatabaseManager, Env

def populate_all_tables() -> None:
    print("Iniciando inserção de dados de teste...")
    try:
        database_commands_manager = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)
        # ==========================================
        # 1. POPULAR USERS
        # ==========================================
        user_fields = ["nome", "email", "tel", "second_tel"]
        users_data = [
            ["Carlos Silva", "carlos.aluno@email.com", "11999998888", None],
            ["Ana Beatriz", "ana.prof@email.com", "11988887777", "1133334444"],
            ["Marcos Souza", "marcos.lib@email.com", "11977776666", None]
        ]
        for user in users_data:
            database_commands_manager._execute_insert("users", user_fields, user)
            database_commands_manager.close_connection()
            
        print("-> Usuários inseridos.")

        # ==========================================
        # 2. POPULAR STUDENTS E EMPLOYEES
        # ==========================================
        # Carlos (ID 1) -> Aluno
        database_commands_manager._execute_insert("students", ["ra", "user_id"], ["RA202612345", 1])
        
        # Ana (ID 2) -> Funcionária (Professora)
        database_commands_manager._execute_insert("employees", ["cpf", "func_id", "job_role"], ["123.456.789-00", 2, "teacher"])
        
        # Marcos (ID 3) -> Funcionário (Bibliotecário)
        database_commands_manager._execute_insert("employees", ["cpf", "func_id", "job_role"], ["987.654.321-11", 3, "library"])

        print("-> Alunos e Funcionários vinculados.")

        # ==========================================
        # 3. POPULAR SERIES
        # ==========================================
        serie_fields = ["name", "description"]
        series_data = [
            ["Crônicas de Fantasia", "Série focada em mundos medievais e mistérios."],
            ["Saga Estelar", "Aventuras de ficção científica no espaço profundo."]
        ]
        for serie in series_data:
            database_commands_manager._execute_insert("series", serie_fields, serie)
            database_commands_manager.close_connection()

        print("-> Séries inseridas.")

        # ==========================================
        # 4. POPULAR AUTHORS
        # ==========================================
        author_fields = ["name", "mini_bio", "img"]
        authors_data = [
            ["J. R. Escritor", "Autor best-seller de literatura fantástica.", "autor1.jpg"],
            ["C. S. Science", "Especialista em contos de ficção científica espacial.", "autor2.jpg"]
        ]
        for author in authors_data:
            database_commands_manager._execute_insert("authors", author_fields, author)
            database_commands_manager.close_connection()

        print("-> Autores inseridos.")

        # ==========================================
        # 5. POPULAR BOOKS
        # ==========================================
        book_fields = ["img", "title", "code", "page_count", "synopsis", "serie_id", "category"]
        books_data = [
            ["livro1.jpg", "O Despertar da Magia", "COD-MAG-01", 350, "O primeiro livro da jornada mágica.", 1, "adventure"],
            ["livro2.jpg", "A Ordem de Orion", "COD-ORI-02", 420, "Uma guerra intergaláctica iminente.", 2, "si-fi"]
        ]
        for book in books_data:
            database_commands_manager._execute_insert("books", book_fields, book)
            database_commands_manager.close_connection()

        print("-> Livros inseridos.")

        # ==========================================
        # 6. POPULAR TABELAS RELACIONAIS (MUITOS PARA MUITOS)
        # ==========================================
        # Autor 1 escreveu o Livro 1 | Autor 2 escreveu o Livro 2
        database_commands_manager._execute_insert("authorXbook", ["author_id", "book_id"], [1, 1])
        database_commands_manager._execute_insert("authorXbook", ["author_id", "book_id"], [2, 2])

        # Autor 1 escreveu a Série 1 | Autor 2 escreveu a Série 2
        database_commands_manager._execute_insert("authorXserie", ["author_id", "serie_id"], [1, 1])
        database_commands_manager._execute_insert("authorXserie", ["author_id", "serie_id"], [2, 2])

        print("-> Relações Autor/Livro/Série mapeadas.")

        # ==========================================
        # 7. POPULAR BOOK_RENTAL_INFO (LOCAÇÕES)
        # ==========================================
        # Usuário 1 (Carlos) alugou o Livro 1 hoje por 7 dias
        rental_fields = ["rental_date", "rental_days", "user_id", "book_id"]
        rental_data = [datetime.date.today(), 7, 1, 1]
        database_commands_manager._execute_insert("book_rental_info", rental_fields, rental_data)

        print("-> Registro de locação criado.")

        # ==========================================
        # 8. POPULAR LOST_ITEMS (ACHADOS E PERDIDOS)
        # ==========================================
        item_fields = ["img", "date_of_acquisition", "title", "description", "type"]
        items_data = [
            ["casaco.jpg", datetime.date.today(), "Casaco de Moletom", "Casaco preto deixado no pátio.", "clothes"],
            ["fone.jpg", datetime.date.today(), "Fone de Ouvido Bluetooth", "Fone estojo branco encontrado na biblioteca.", "electronic"]
        ]
        for item in items_data:
            database_commands_manager._execute_insert("lost_items", item_fields, item)
            database_commands_manager.close_connection()

        print("-> Itens achados e perdidos registrados.")

        # Se tudo rodar perfeitamente, salva as alterações
        database_commands_manager._execute_commit()
        print("\n[SUCESSO] Todas as tabelas foram populadas com sucesso!")

    except Exception as e:
        database_commands_manager._excute_rollback()
        print(f"\n[ERRO] Falha ao popular as tabelas. Rollback executado. Motivo: {e}")
        