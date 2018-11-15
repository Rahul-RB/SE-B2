from flask import Flask
from flaskext.mysql import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

mysql = MySQL()
mysql.init_app(app)
	
from hawkeye import views
	
	

