from mysql.connector import Error
from mysql.connector.types import RowItemType, RowType
from typing import List, Dict, Any
from .database_connection_manager import DatabaseConnectionManager

class DatabaseCommandsManager(DatabaseConnectionManager):
	def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
		super().__init__(host, port, database, user, password)

	def __format_where_query(self, where_query) -> str:
		where_query_striped = where_query.strip()
		where_query_formated = where_query_striped if where_query_striped.startswith("WHERE") or where_query_striped == "" else f"WHERE {where_query}"

		return where_query_formated
	
	def _create_if_not_exist_table(self, table_name: str, fields: List[str]) -> None:
		fields_str = ", ".join(fields)
		
		create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})"

		_, cursor = self.get_connection()
		
		cursor.execute(create_table_query)

	def _execute_insert(self, table: str, fields: List[str], values: List[Any]) -> None:
		table_fields_str = ", ".join(fields)
		insert_query_without_values = f"INSERT INTO {table} ({table_fields_str})"

		template_values = ", ".join(["%s"] * len(fields))
		insert_query_with_template_values = f"{insert_query_without_values} VALUES ({template_values})"

		_, cursor = self.get_connection()
		
		cursor.execute(insert_query_with_template_values, values)

	def _execute_delete(self, table: str, where_query: str, values: List[Any]) -> int:
		basic_delete_instrution = f"DELETE FROM {table}"

		where_query_formated = self.__format_where_query(where_query)

		complete_delete_instrution = f"{basic_delete_instrution} {where_query_formated}"

		_, cursor = self.get_connection()
		
		cursor.execute(complete_delete_instrution, values)

		return cursor.rowcount

	def _execute_select(self, table: str, fields: List[str], where_query="", values: List[Any]=[]) -> List[RowType | Dict[str, RowItemType]] | Any:
		table_fields_str = ", ".join(fields)
		select_query = f"SELECT {table_fields_str} FROM {table}"

		where_query_formated = self.__format_where_query(where_query)

		select_query_complete = f"{select_query} {where_query_formated}"

		_, cursor = self.get_connection()

		cursor.execute(select_query_complete, values)
		data = cursor.fetchall()

		self.close_current_connection()

		return data

	def _excute_rollback(self) -> None:
		try:
			if self.current_connection is not None:
				self.current_connection.rollback()
			print(f"Completed rollback")
		except Error as rollback_err:
			print(f"Error while executing rollback: {rollback_err}")
		
		self.close_current_connection()
	
	def _execute_commit(self) -> None:
			try:
				self.current_connection.commit()
			except Error as commit_err:
				print(f"Error while executing commit: {commit_err}")

				self._excute_rollback()

			self.close_current_connection()