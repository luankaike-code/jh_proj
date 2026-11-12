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

        self.current_connection = None
        self.current_cursor = None

        self._connection_pool = self._create_connection_pool()

    def get_connection(self) -> tuple[PooledMySQLConnection, MySQLCursorBufferedDict]:
        if not self._connection_pool:
            raise RuntimeError("O pool de conexões não foi inicializado corretamente.")
            
        connection = self._connection_pool.get_connection()
        cursor = connection.cursor(buffered=True, dictionary=True)

        self.current_connection = connection
        self.current_cursor = cursor  

        return connection, cursor 

    def close_current_connection(self) -> None:
        if self.current_cursor is not None:
            try:
                self.current_cursor.close()
            except Exception:
                pass
            finally:
                self.current_cursor = None

        if self.current_connection is not None:
            try:
                if hasattr(self.current_connection, 'is_connected') and self.current_connection.is_connected():
                    self.current_connection.close()
            except Exception:
                pass
            finally:
                self.current_connection = None

    def close_all_connections(self) -> None:
        if self._connection_pool and hasattr(self._connection_pool, '_remove_connections'):
            try:
                self._connection_pool._remove_connections()
            except Exception:
                pass

    def _create_connection_pool(self) -> pooling.MySQLConnectionPool | None:
        connection_pool = None
        connection_attempts = 0

        while connection_attempts < MAX_CONNECTION_ATTEMPS and connection_pool is None:
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
                connection_attempts += 1
                print(f"Error #{connection_attempts} thrown while connecting to MySQL: {e}; attempting again...")

        return connection_pool

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_current_connection()