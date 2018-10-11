from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"]=True

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'RahulRB@1997'# Put your MySQL root password here
app.config['MYSQL_DATABASE_DB'] = 'Hawkeye'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


from hawkeye import views