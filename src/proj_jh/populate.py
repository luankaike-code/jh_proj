import datetime
from db import DatabaseManager, Env

def populate_users(Env) -> bool:
    db = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)
    try:
        user_fields = ["nome", "email", "tel", "second_tel"]
        users_data = [
            ["Carlos Silva", "carlos.aluno@email.com", "11999998888", None],
            ["Ana Beatriz", "ana.prof@email.com", "11988887777", "1133334444"],
            ["Marcos Souza", "marcos.lib@email.com", "11977776666", None]
        ]
        for user in users_data:
            try:
                db._execute_insert("users", user_fields, user)
                db._execute_commit()
            except Exception as insert_err:
                if "1062" in str(insert_err):
                    print(f"[INFO] Usuário {user[1]} já cadastrado.")
                else:
                    raise insert_err
                   
        print("-> Usuários processados com sucesso.")
        return True
    except Exception as e:
        db._excute_rollback()
        print(f"[ERRO] Falha ao inserir usuários: {e}")
        return False
    finally:
        db.close_current_connection()

def populate_students_and_employees(Env) -> bool:
    db = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)
    try:
        # 1. Busca o ID do Carlos dinamicamente pelo e-mail usando _execute_select
        carlos = db._execute_select(
            table="users", 
            fields=["id"], 
            where_query="WHERE email = %s", 
            values=["carlos.aluno@email.com"]
        )
        
        # 2. Busca o ID da Ana
        ana = db._execute_select(
            table="users", 
            fields=["id"], 
            where_query="WHERE email = %s", 
            values=["ana.prof@email.com"]
        )
        
        # 3. Busca o ID do Marcos
        marcos = db._execute_select(
            table="users", 
            fields=["id"], 
            where_query="WHERE email = %s", 
            values=["marcos.lib@email.com"]
        )

        if not carlos or not ana or not marcos:
            raise Exception("Usuários pais não encontrados no banco para realizar os vínculos!")

        # Extrai os IDs reais retornados (como usamos dictionary=True, acessamos pela chave 'id')
        carlos_id = carlos[0]["id"]
        ana_id = ana[0]["id"]
        marcos_id = marcos[0]["id"]

        # Insere utilizando os IDs reais do banco
        # 1. Inserir Estudante (Carlos)
        try:
            db._execute_insert("students", ["ra", "user_id"], ["RA202612345", carlos_id])
            db._execute_commit()
            print("-> Estudante inserido com sucesso.")
        except Exception as insert_err:
            if "1062" in str(insert_err):
                db._excute_rollback()
                print("[INFO] Estudante com este RA já existe. Ignorando...")
            else:
                raise insert_err

        # 2. Inserir Funcionário (Ana)
        try:
            db._execute_insert("employees", ["cpf", "func_id", "job_role"], ["123.456.789-00", ana_id, "teacher"])
            db._execute_commit()
            print("-> Professor inserido com sucesso.")
        except Exception as insert_err:
            if "1062" in str(insert_err):
                db._excute_rollback()
                print("[INFO] Funcionário com este CPF já existe. Ignorando...")
            else:
                raise insert_err

        # 3. Inserir Funcionário (Marcos)
        try:
            db._execute_insert("employees", ["cpf", "func_id", "job_role"], ["987.654.321-11", marcos_id, "library"])
            db._execute_commit()
            print("-> Bibliotecário inserido com sucesso.")
        except Exception as insert_err:
            if "1062" in str(insert_err):
                db._excute_rollback()
                print("[INFO] Funcionário com este CPF já existe. Ignorando...")
            else:
                raise insert_err
        
        print("-> Alunos e Funcionários vinculados com sucesso.")
        return True
    except Exception as e:
        db._excute_rollback()
        print(f"[ERRO] Falha ao vincular alunos/funcionários: {e}")
        return False
    finally:
        db.close_current_connection()

def populate_series(Env) -> bool:
    db = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)
    try:
        serie_fields = ["name", "description"]
        series_data = [
            ["Crônicas de Fantasia", "Série focada em mundos medievais e mistérios."],
            ["Saga Estelar", "Aventuras de ficção científica no espaço profundo."]
        ]
        for serie in series_data:
            try:
                db._execute_insert("series", serie_fields, serie)
                db._execute_commit()
            except Exception as insert_err:
                if "1062" in str(insert_err):
                    print(f"[INFO] Série '{serie[0]}' já existe.")
                else:
                    raise insert_err
                    
        print("-> Séries processadas com sucesso.")
        return True
    except Exception as e:
        db._excute_rollback()
        print(f"[ERRO] Falha ao inserir séries: {e}")
        return False
    finally:
        db.close_current_connection()

def populate_books(Env) -> bool:
    db = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)
    try:
        # Busca a série de fantasia dinamicamente para pegar o ID correto
        serie_fantasia = db._execute_select(
            table="series", 
            fields=["id"], 
            where_query="WHERE name = %s", 
            values=["Crônicas de Fantasia"]
        )
        serie_estelar = db._execute_select(
            table="series", 
            fields=["id"], 
            where_query="WHERE name = %s", 
            values=["Saga Estelar"]
        )

        if not serie_fantasia or not serie_estelar:
            raise Exception("Séries necessárias não encontradas para vincular aos livros!")

        id_fantasia = serie_fantasia[0]["id"]
        id_estelar = serie_estelar[0]["id"]

        book_fields = ["img", "title", "code", "page_count", "synopsis", "serie_id", "category"]
        books_data = [
            ["livro1.jpg", "O Despertar da Magia", "COD-MAG-01", 350, "O primeiro livro da jornada mágica.", id_fantasia, "adventure"],
            ["livro2.jpg", "A Ordem de Orion", "COD-ORI-02", 420, "Uma guerra intergaláctica iminente.", id_estelar, "si-fi"]
        ]
        
        for book in books_data:
            try:
                db._execute_insert("books", book_fields, book)
            except Exception as insert_err:
                if "1062" in str(insert_err):
                    print(f"[INFO] Livro '{book[1]}' já existe.")
                else:
                    raise insert_err

        db._execute_commit()
        print("-> Livros processados com sucesso.")
        return True
    except Exception as e:
        db._excute_rollback()
        print(f"[ERRO] Falha ao inserir livros: {e}")
        return False
    finally:
        db.close_current_connection()

def populate_all_tables() -> None:
    print("Iniciando rotina de população de dados...")
    
    populate_users(Env)
    populate_students_and_employees(Env)
    populate_series(Env)
    populate_books(Env)
    
    print("\n[FINALIZADO] Processo de população concluído.")