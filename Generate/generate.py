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
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'


def create_connection():
    conn = None
    try:
        if not os.path.exists("logs.db"):
            conn = sqlite3.connect('logs.db')
        else:
            conn = sqlite3.connect('logs.db')
        return conn
    except Error as e:
        print(e)
    return conn


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("private_key.pem", "wb") as f:
        f.write(pem)


def save_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("public_key.pem", "wb") as f:
        f.write(pem)


def load_private_key():
    if os.path.isfile("private_key.pem"):
        with open("private_key.pem", "rb") as f:
            pem = f.read()
            return serialization.load_pem_private_key(pem, password=None, backend=default_backend())
    else:
        return None


def load_public_key():
    if os.path.isfile("public_key.pem"):
        with open("public_key.pem", "rb") as f:
            pem = f.read()
            return serialization.load_pem_public_key(pem, backend=default_backend())
    else:
        return None


private_key = load_private_key()
public_key = load_public_key()
if private_key is None or public_key is None:
    private_key, public_key = generate_key_pair()
    save_private_key(private_key)
    save_public_key(public_key)


@app.before_request
def before_request():
    g.private_key = private_key
    g.public_key = public_key

# Function to generate a QR code


def generate_qr_code(data, output_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(output_file)

# Function to read a QR code from an image


def read_qr_code(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Create a QR code detector
    detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(
        img)

    if retval:
        return decoded_info
    else:
        return None


class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = str(data)
        self.previous_hash = previous_hash
        self.current_hash = self.hash_block()
        self.encrypted_data = None
        self.decrypted_data = None

    def encrypt_data(self, public_key):
        data_bytes = self.data.encode()
        encrypted_data = public_key.encrypt(
            data_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.encrypted_data = encrypted_data.hex()

    def decrypt_data(self, private_key):
        try:
            encrypted_data = bytes.fromhex(self.encrypted_data)
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            self.decrypted_data = decrypted_data.decode()
        except Exception as e:
            print(e)

    def hash_block(self):
        input_string = f"{self.timestamp}{self.data}{self.previous_hash}"
        input_bytes = input_string.encode()
        hash_bytes = hashlib.sha256(input_bytes)
        hash_hex = hash_bytes.hexdigest()
        return hash_hex


class Blockchain:

    counter = 0

    def __init__(self):
        self.chain = self.load_blocks_from_db()

    def load_blocks_from_db(self):
        conn = create_connection()
        with conn:
            c = conn.cursor()
            try:
                c.execute("SELECT * FROM blocks")
                rows = c.fetchall()

                blocks = []
                for row in rows:
                    timestamp, encrypted_data, previous_hash, current_hash = row
                    new_block = Block(timestamp, "", previous_hash)
                    new_block.encrypted_data = encrypted_data
                    new_block.current_hash = current_hash
                    blocks.append(new_block)

                return blocks
            except sqlite3.OperationalError:
                return []

    def add_block(self, data, public_key):
        Blockchain.counter += 1
        timestamp = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=5, minutes=30))).strftime("%a %b %d %H:%M:%S %Y")
        previous_hash = self.chain[-1].current_hash if self.chain else ""
        new_block = Block(timestamp, data, previous_hash)
        new_block.encrypt_data(public_key)
        self.chain.append(new_block)
        self.save_to_db(new_block)
        self.return_the_hash(new_block)
        self.create_qr_code(new_block)

    def save_to_db(self, block):
        conn = create_connection()
        with conn:
            create_table(conn)
            c = conn.cursor()
            c.execute("INSERT INTO blocks (timestamp, encrypted_data, previous_hash, current_hash) VALUES (?, ?, ?, ?)",
                      (block.timestamp, block.encrypted_data, block.previous_hash, block.current_hash))
            conn.commit()

    def return_the_hash(self, block):

        file_path = "hash.txt"
        text_to_add = block.encrypted_data
        try:
            with open(file_path, "a") as file:
                file.writelines(text_to_add + "\n")
        except FileNotFoundError:
            with open(file_path, "w") as file:
                file.writelines(text_to_add + "\n")

    def create_qr_code(self, block):

        file_path_qr = f"static/qr_code_{Blockchain.counter}.png"
        data_to_be_encoded = block.encrypted_data

        generate_qr_code(data_to_be_encoded, file_path_qr)


def create_table(conn):
    try:
        c = conn.cursor()
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS blocks
            ("timestamp" TEXT PRIMARY KEY, encrypted_data TEXT, previous_hash TEXT, current_hash TEXT)
        '''
        c.execute(create_table_sql)
    except Error as e:
        print(e)


blockchain = Blockchain()


@app.route("/")
def index():
    private_key = g.private_key

    blocks = []
    for block in blockchain.chain:
        if block.timestamp == 0:
            continue
        if block.decrypted_data is None:
            block.decrypt_data(private_key)

        block_dict = {
            "timestamp": block.timestamp,
            "data": block.decrypted_data,
            "previous_hash": block.previous_hash,
            "current_hash": block.current_hash
        }
        blocks.append(block_dict)

    # return render_template("index.html", blocks=blocks)
    return render_template("index.html")


@app.route("/add_block", methods=["POST"])
# @cross_origin()
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def add_block():
    if request.method == 'POST':
        # Retrieve the form data submitted by the user
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

        public_key = g.public_key

        blockchain.add_block(jsonify(data), public_key)
        generated_qr_code = f"qr_code_{blockchain.counter}.png"

        response_data = {
            "qr_code": generated_qr_code
        }

        print(response_data)

        # return jsonify(response_data)
        # return f"qr_code: {generated_qr_code}"
        return app.response_class(
            response=json.dumps(response_data),
            status=200,
            mimetype="application/json"
        )
    return redirect(url_for("index"))


@app.route("/validate_block", methods=["POST"])
def validate_block():
    # TODO: validate the certificate
    pass


if __name__ == "__main__":
    # block_thread = threading.Thread(target=generate_block_every_second)
    # block_thread.daemon = True
    # block_thread.start()
    app.run(debug=True)
