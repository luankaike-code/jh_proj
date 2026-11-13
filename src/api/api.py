from flask import Flask
from .routes import book_blueprint, serie_blueprint, user_blueprint

app = Flask(__name__)

class Api:
	@staticmethod
	def all_regsiter_routes():
		app.register_blueprint(book_blueprint)
		app.register_blueprint(serie_blueprint)
		app.register_blueprint(user_blueprint)

	@staticmethod
	def start():
		Api.all_regsiter_routes()
		
		app.run(
			debug=True,
			port=5000
		)