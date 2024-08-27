from flask import Flask, request, jsonify,render_template
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route("/")
def index():
    return "Index"

@app.route("/hello")
def hello():
    return render_template('hello.html')

@app.route('/estimate_height', methods=['POST'])
def estimate_height():
    image_data = request.files['image'].read()
    image = Image.open(BytesIO(image_data))
    image = np.array(image)

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection (simple method for now)
    edges = cv2.Canny(gray, 50, 150)

    # Detect lines using Hough transform (simplistic approach)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    estimated_height = 1.75  # Dummy height

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Calculate pixel distance between the detected lines
            pixel_distance = abs(y2 - y1)
            real_world_distance = 1.7  # in meters
            known_pixel_distance = 500  # pixels
            estimated_height = (pixel_distance / known_pixel_distance) * real_world_distance

    return jsonify({"estimated_height": estimated_height})

if __name__ == '__main__':
    app.run(debug=True)