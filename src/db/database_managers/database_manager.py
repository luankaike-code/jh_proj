from .database_commands_manager import DatabaseCommandsManager

class DatabaseManager(DatabaseCommandsManager):
	def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
		super().__init__(host, port, database, user, password)