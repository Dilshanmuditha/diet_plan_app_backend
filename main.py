# from flask import Flask, request, jsonify
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_mysqldb import MySQL
# from datetime import timedelta

# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# # MySQL Configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'fitnessapp'

# mysql = MySQL(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# # Register route
# @app.route('/register', methods=['POST'])
# def register():
#     name = request.json.get('name')
#     password = request.json.get('password')
#     email = request.json.get('email')

#     if not name or not password or not email:
#         return jsonify({"msg": "Missing name, password, or email"}), 400

#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
#     existing_user = cursor.fetchone()

#     if existing_user:
#         return jsonify({"msg": "User already exists"}), 400

#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#     cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)",
#                    (name, hashed_password, email))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({"msg": "User registered successfully"}), 201

# # Login route
# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email')
#     password = request.json.get('password')

#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#     user = cursor.fetchone()
#     cursor.close()

#     if not user or not bcrypt.check_password_hash(user[3], password):
#         return jsonify({"msg": "Bad email or password"}), 401

#     access_token = create_access_token(identity=user[2])
#     return jsonify(access_token=access_token), 200

# # Get user profile
# @app.route('/profile', methods=['GET'])
# @jwt_required()
# def profile():
#     current_user = get_jwt_identity()
#     # return jsonify(logged_in_as=current_user), 200

#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT id, name, email, created_at FROM users WHERE email = %s", (current_user,))
#     user = cursor.fetchone()
#     cursor.close()

#     return jsonify({"id": user[0], "name": user[1], "email": user[2], "created_at": user[3]}), 200

# # Update user profile
# @app.route('/profile', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     current_user = get_jwt_identity()
#     name = request.json.get('name')

#     cursor = mysql.connection.cursor()
#     cursor.execute("UPDATE users SET name = %s WHERE email = %s", (name, current_user))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({"msg": "Profile updated successfully"}), 200

# # Delete user account
# @app.route('/profile', methods=['DELETE'])
# @jwt_required()
# def delete_profile():
#     current_user = get_jwt_identity()

#     cursor = mysql.connection.cursor()
#     cursor.execute("DELETE FROM users WHERE email = %s", (current_user,))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({"msg": "User deleted successfully"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)