from proj_jh.initialization import initialization_tables
from proj_jh.populate import populate_all_tables
from api import Api

print("1")
initialization_tables()
print("2")
populate_all_tables()
print("3")
Api.start()