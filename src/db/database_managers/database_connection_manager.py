import os
from mysql.connector import Error, pooling
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.cursor import MySQLCursorBufferedDict

MAX_CONNECTION_ATTEMPS = 5

class DatabaseConnectionManager:
	def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
		self.__host = host
		self.__port = port
		self.__database = database
		self.__user = user
		self.__password = password

		self._connection_pool = self._create_connection_pool()

	def get_connection(self) -> tuple[PooledMySQLConnection, MySQLCursorBufferedDict]:
		connection: PooledMySQLConnection = self._connection_pool.get_connection()
		cursor: MySQLCursorBufferedDict = connection.cursor(buffered=True, dictionary=True)

		self.current_connection = connection
		self.current_cursor = cursor

		return connection, cursor

	def close_connection(self) -> None:
		self.current_cursor.close()
		self.current_connection.close()

	def _create_connection_pool(self) -> pooling.MySQLConnectionPool | None:
		connection_pool = None
		connection_attemps = 0

		while connection_attemps < MAX_CONNECTION_ATTEMPS and connection_pool == None:
			try:
				connection_pool = pooling.MySQLConnectionPool(
					pool_name="connection_pool",
					pool_size=5,
					host=self.__host,
					port=self.__port,
					database=self.__database,
					user=self.__user,
					password=self.__password,
				)
			except Error as e:
				connection_attemps += 1
				print(f"Error #{connection_attemps} throw while connecting to MySQL: {e}; attempting again...")

		return connection_pool

	def __del__(self) -> None:
		if 'connection' in locals() and self._connection.is_connected():
			self._cursor.close()
			self._connection.close()
			print("MySQL connection is closed.")