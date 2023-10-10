import hashlib
import os
from flask import Flask, render_template, current_app, request, redirect, url_for, g, jsonify, json
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
from flask_cors import CORS, cross_origin
import json
import requests

port = "5050"

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'


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


def is_data_present(data_to_check):
    try:
        #c = conn.cursor()
        query = f"SELECT COUNT(*) FROM blocks WHERE encrypted_data = '{data_to_check}'"
        response = requests.post('http://localhost:5000/api/query', json={'query': query})
        result = response.json()

        if result[0][0] > 0:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
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
    # conn = sqlite3.connect('../Generate/logs.db')
    # c = conn.cursor()

    # Execute the SQL query to fetch the current_hash from the database
    query = f"SELECT current_hash FROM blocks WHERE encrypted_data = '{encrypted_data}'"
    response = requests.post('http://localhost:5000/api/query', json={'query': query})
    result = response.json()

    if result:
        return result[0][0]  # Return the value of the current_hash column
    else:
        return None  # Return None if no row is found for the encrypted data


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def index():
    if request.method == 'POST':
        data = {
            "courseid": request.form['courseid'],
            "coursename": request.form['coursename'],
            "email": request.form['email'],
            "enddate": request.form['enddate'],
            "instname": request.form['instname'],
            "name": request.form['name'],
            "phnumber": request.form['phnumber'],
            "startdate": request.form['startdate'],
        }

        # Extract QR code content from uploaded image (you'll need a QR code library)
        file = request.files['certificate']

        # Set the directory path for storing the uploaded files
        upload_directory = './static/uploads'

        # Save the file to the specified directory
        file.save(os.path.join(upload_directory, file.filename))

        # Optionally, you can also store the filepath in a variable for further processing or database storage
        filepath = os.path.join(upload_directory, file.filename)

        encrypted_data = read_qr_code(filepath)

        print(type(data))
        print(data)

        data_str = json.dumps(data)

        private_key = load_private_key()

        print(encrypted_data)

        if is_data_present(encrypted_data):
            print("H1")
            real_data = decrypt_data(encrypted_data, private_key)
            print(encrypted_data)
            print(real_data)
            print(str(data_str))

            if str(data_str) == real_data:
                print("valid")
                signature = get_current_hash(encrypted_data)
                print(signature)
                response_data = {
                    "signature": signature
                }
                return app.response_class(
                    response=json.dumps(response_data),
                    status=200
                )
            else:
                print("H2")
                return app.response_class(
                    response=json.dumps("Not Valid"),
                    status=400
                )
        else:
            print("H3")
            return app.response_class(
                response=json.dumps("Not Valid"),
                status=400
            )

    return render_template('index_2.html')


if __name__ == '__main__':
    app.run(port=port, debug=True)
