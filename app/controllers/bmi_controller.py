from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from werkzeug.security import check_password_hash
class BMICalculator:
    
    @staticmethod
    def bmiCalculate():
        height = float(request.json.get('height'))
        weight = float(request.json.get('weight'))
        x = weight/float(height*height)
        if x < 18.5:
            return jsonify({"msg": "User is Underweight", "data":x}), 200
        if x>=18.5 and x < 25:
            return jsonify({"msg": "User is Normal", "data":x}), 200
        if x >= 25 and x < 30:
            return jsonify({"msg": "User is Overweight", "data":x}), 200
        if x >= 30:
            return jsonify({"msg": "User is Obesity", "data":x}), 200
        
    @staticmethod
    @jwt_required()
    def bmiSave():
        current_user = get_jwt_identity()

        user = User.get_user_by_email(current_user)
        if not user:
            return jsonify({"msg": "User not found"}), 404
        bmi = request.json.get('bmi')

        User.add_user_bmi(user[0], bmi)
        updated_user = User.get_user_by_email(current_user)
        data = {
            "id": updated_user[0],
            "name": updated_user[1],
            "email": updated_user[2],
            "dob": updated_user[4],
            "mobile": updated_user[5],
            "address": updated_user[6],
            "sex": updated_user[7],
            "bmi": updated_user[8],
            "created_at": updated_user[9]
            }
        return jsonify({"msg": "User bmi details updated successfully","data": data}), 201