from db  import DatabaseManager, Env

datbase_manager = DatabaseManager(Env.HOST, Env.PORT, Env.DATABASE, Env.USER, Env.PASSWORD)