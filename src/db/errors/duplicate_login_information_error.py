from typing import List

class DuplicateLoginInformationError(Exception):
	def __init__(self, table: str, count: int, logins_informations: List):
		super().__init__(f"Have {count} duplicate login information in {table}`s table. logins informations: {logins_informations}")