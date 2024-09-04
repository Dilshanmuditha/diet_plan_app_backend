from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()

class User:
    @staticmethod
    def create_user(name, email, password):
        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_user_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def update_user(user_id, email, name, password):
        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET email = %s,name = %s, password = %s WHERE id = %s", (email,name, hashed_password, user_id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete_user(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
    
    @staticmethod
    def add_user_details(user_id, dob, mobile, address, sex, bmi):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET dob = %s,mobile = %s, address = %s, sex = %s, bmi = %s WHERE id = %s", (dob, mobile, address, sex, bmi, user_id))
        mysql.connection.commit()
        cursor.close()