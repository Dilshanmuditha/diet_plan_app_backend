from flask import Blueprint,render_template, Response, request, jsonify
from app.controllers.user_controller import UserController
from app.controllers.bmi_controller import BMICalculator
from flask_jwt_extended import jwt_required, get_jwt
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
BLACKLIST = set()
user = Blueprint('user', __name__)
bmi = Blueprint('bmi', __name__)
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

@user.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # JWT ID, a unique identifier for the token
    BLACKLIST.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

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

@user.route('/add-user-details', methods=['PUT'])
@jwt_required()
def add_user_details():
    return UserController.add_user_details()

@bmi.route("/hello")
def hello():
    return render_template('index.html')

@bmi.route("/bmi-calculate", methods=['POST'])
def bmi_calculate():
    return BMICalculator.bmiCalculate()

@bmi.route("/bmi-save", methods=['POST'])
def bmi_save():
    return BMICalculator.bmiSave()
 
@bmi.route('/estimate_height', methods=['POST'])
def estimate_height():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Load pre-trained model (ensure you have the correct paths)
    net = cv2.dnn.readNetFromCaffe('pose_deploy.prototxt', 'pose_iter_440000.caffemodel')
    
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    output = net.forward()
    
    # Extract keypoints (assuming the model outputs keypoints)
    points = []
    for i in range(len(output[0, 0])):
        probMap = output[0, 0, i]
        minVal, probMap, minLoc, point = cv2.minMaxLoc(probMap)
        x = (w * point[0]) / w
        y = (h * point[1]) / h
        points.append((int(x), int(y)))
    
    if len(points) < 2:
        return jsonify({"error": "Could not detect keypoints for height estimation"}), 400
    
    # Assuming points[0] is head and points[1] is feet
    head = points[0]
    feet = points[1]
    height_pixels = np.linalg.norm(np.array(head) - np.array(feet))
    
    # Convert pixel height to actual height (requires calibration)
    height_meters = height_pixels / 100.0
    return jsonify({"height_meters": round(height_meters, 2)})