from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager

mysql = MySQL()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'fitnessapp'

    mysql.init_app(app)
    jwt.init_app(app)

    from app.views import user, main

    app.register_blueprint(user)
    app.register_blueprint(main) 
    
    return app