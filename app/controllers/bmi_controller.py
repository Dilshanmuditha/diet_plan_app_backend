from flask import jsonify, request

class BMICalculator:
    
    @staticmethod
    def bmiCalculate():
        height = float(request.json.get('height'))
        weight = float(request.json.get('weight'))
        x = weight/float(height*height)
        if x < 18.5:
            return jsonify({"msg": "User is Underweight"}), 200
        if x>=18.5 and x < 25:
            return jsonify({"msg": "User is Normal"}), 200
        if x >= 25 and x < 30:
            return jsonify({"msg": "User is Overweight"}), 200
        if x >= 30:
            return jsonify({"msg": "User is Obesity"}), 200