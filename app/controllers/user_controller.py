from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from werkzeug.security import check_password_hash

class UserController:

    @staticmethod
    def register():
        username = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')

        if User.get_user_by_email(email):
            return jsonify({"msg": "email already exists"}), 409

        User.create_user(username,email, password)
        return jsonify({"msg": "User created successfully"}), 201

    @staticmethod
    def login():
        email = request.json.get('email')
        password = request.json.get('password')
        
        user = User.get_user_by_email(email)
        if not user or not check_password_hash(user[3], password):
            return jsonify({"msg": "Invalid email or password"}), 401

        access_token = create_access_token(identity=email)
        data = {"first_name": user[1], "last_name": user[2]}
        return jsonify({"msg": "Login successful", "data": data, "token": access_token}), 200


    @staticmethod
    @jwt_required()
    def get_current_user():
        current_user = get_jwt_identity()
        user = User.get_user_by_email(current_user)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        return jsonify({
            "id": user[0],
            "user": user[1],
            "email": user[2],
            "created_at": user[3]
        }), 200

    @staticmethod
    @jwt_required()
    def update_user():
        current_user = get_jwt_identity()
        new_email = request.json.get('email')
        new_name = request.json.get('name')
        new_password = request.json.get('password')

        user = User.get_user_by_email(current_user)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        User.update_user(user[0], new_name, new_email, new_password)
        return jsonify({"msg": "User updated successfully"}), 200

    @staticmethod
    @jwt_required()
    def delete_user():
        current_user = get_jwt_identity()
        user = User.get_user_by_email(current_user)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        User.delete_user(user[0])
        return jsonify({"msg": "User deleted successfully"}), 200
    
    @staticmethod
    @jwt_required()
    def add_user_details():
        current_user = get_jwt_identity()

        user = User.get_user_by_email(current_user)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        dob = request.json.get('dob')
        mobile = request.json.get('mobile')
        address = request.json.get('address')
        sex = request.json.get('sex')
        bmi = request.json.get('bmi')

        User.add_user_details(user[0], dob, mobile, address, sex, bmi)
        return jsonify({"msg": "User details updated successfully"}), 201