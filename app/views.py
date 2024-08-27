from flask import Blueprint,render_template, Response
from app.controllers.user_controller import UserController
from flask_jwt_extended import jwt_required

user = Blueprint('user', __name__)
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@user.route('/register', methods=['POST'])
def register():
    return UserController.register()

@user.route('/login', methods=['POST'])
def login():
    return UserController.login()

@user.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    return UserController.get_current_user()

@user.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    return UserController.update_user()

@user.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    return UserController.delete_user()