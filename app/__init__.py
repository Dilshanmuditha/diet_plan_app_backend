from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager

mysql = MySQL()
jwt = JWTManager()
BLACKLIST = set()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'fitnessapp'

    mysql.init_app(app)
    jwt.init_app(app)

    from app.views import user, main, bmi

    app.register_blueprint(user)
    app.register_blueprint(main) 
    app.register_blueprint(bmi) 
    
    return app

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLIST