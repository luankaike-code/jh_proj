from proj_jh.initialization import initialization_tables
from proj_jh.populate import populate_all_tables
from api import Api

initialization_tables()
populate_all_tables()
Api.start()