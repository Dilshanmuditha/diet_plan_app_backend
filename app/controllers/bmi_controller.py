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
        return jsonify({"msg": "User bmi details updated successfully"}), 201