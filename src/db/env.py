from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Env:
	HOST = os.getenv("HOST")
	USER = os.getenv("USER")
	PORT = int(os.getenv("PORT"))
	PASSWORD = os.getenv("PASSWORD")
	DATABASE = os.getenv("DATABASE")