import hashlib
import os
from flask import Flask, render_template, current_app, request, redirect, url_for, g
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import sqlite3
from sqlite3 import Error
import time
import datetime
from time import ctime, sleep
import threading
import qrcode
import cv2
from pyzbar.pyzbar import decode


port = "5050"

app = Flask(__name__)

def load_private_key():
    if os.path.isfile("private_key.pem"):
        with open("private_key.pem", "rb") as f:
            pem = f.read()
            return serialization.load_pem_private_key(pem, password=None, backend=default_backend())
    else:
        return None

private_key = load_private_key()

if private_key is None:
    raise Exception("Private key is not found!!")

def read_qr_code(image_path):
    # Load the image containing the QR code
    image = cv2.imread(image_path)

    # Decode the QR code
    decoded_objects = decode(image)

    # Check if any QR code was found in the image
    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            qr_type = obj.type
            return qr_data
    else:
        return None

def is_data_present(conn, data_to_check):
    try:
        c = conn.cursor()
        query = "SELECT COUNT(*) FROM blocks WHERE encrypted_data = ?"
        c.execute(query, (data_to_check,))
        result = c.fetchone()[0]

        if result > 0:
            return True
        else:
            return False

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

def decrypt_data(encrypted_data_hex, private_key):
    try:
        encrypted_data = bytes.fromhex(encrypted_data_hex)
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode()
    except Exception as e:
        print(e)

def get_current_hash(encrypted_data):
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    # Execute the SQL query to fetch the current_hash from the database
    c.execute("SELECT current_hash FROM blocks WHERE encrypted_data=?", (encrypted_data,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the value of the current_hash column
    else:
        return None  # Return None if no row is found for the encrypted data



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phnumber': request.form['phnumber'],
            'coursename': request.form['coursename'],
            'courseid': request.form['courseid'],
            'instname': request.form['instname'],
            'startdate': request.form['startdate'],
            'enddate': request.form['enddate']
        }

        
        # Extract QR code content from uploaded image (you'll need a QR code library)
        file = request.files['certificate']

        # Set the directory path for storing the uploaded files
        upload_directory = 'C:\\Users\\Mayukh Mondal\\Desktop\\BlockVerificationSystem\\'                                     #Anish Change the path

        # Save the file to the specified directory
        file.save(os.path.join(upload_directory, file.filename))

        # Optionally, you can also store the filepath in a variable for further processing or database storage
        filepath = os.path.join(upload_directory, file.filename)

        encrypted_data = read_qr_code("certificate.png")

        print(type(data))
        print(data)

        data_str = str(data)

        private_key = load_private_key()
        
        db_path = "logs.db"
        conn = sqlite3.connect(db_path)
        # Check if the QR code content exists in the database
        if is_data_present(conn, encrypted_data):
            real_data = decrypt_data(encrypted_data, private_key)
            print(encrypted_data)
            print(real_data)
            
            if (data_str == real_data):
                signature = get_current_hash(encrypted_data)
                print(signature)
                return render_template('valid.html', signature=signature)
            else:
                return render_template('not_valid.html')
            
        else:
            return render_template('not_valid.html')
            
    
    return render_template('index_2.html')

if __name__ == '__main__':
    app.run(port=port, debug=True)
