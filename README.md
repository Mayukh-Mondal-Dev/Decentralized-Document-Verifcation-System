# Decentralized-Document-Verifcation-System
<h1>Flask Blockchain Application</h1>
The project is a web-based certificate generation and validation system using Flask. It encrypts user-submitted certificate data, stores it in a blockchain, and generates a QR code for verification. The validation component decrypts data, checks it against the blockchain, and confirms certificate authenticity.
This README provides step-by-step instructions on setting up and running a Flask-based blockchain web application for creating and validating digital certificates. The application allows you to add certificate information, encrypt it, and store it in a blockchain. It also generates QR codes for each certificate for easy retrieval and validation.

Prerequisites:

Python 3.x installed on your system.

Basic understanding of Python, Flask, and SQLite.

Ensure you have the required Python packages installed. You can install them using pip:

Copy code
pip install Flask cryptography qrcode opencv-python-headless flask-cors
Steps:

Clone the Repository:

Clone the repository to your local machine using Git:

bash
Copy code
git clone https://github.com/yourusername/blockchain-web-app.git
Replace yourusername with your actual GitHub username.

Navigate to the Project Directory:

bash
Copy code
cd blockchain-web-app
Generate Key Pairs:

The application uses public-key cryptography for encryption. It generates key pairs for encryption and stores them in private_key.pem and public_key.pem files. Run the following command to generate the keys:

Copy code
python app.py
Run the Application:

Start the Flask application by running:

Copy code
python app.py
This will start the application on http://127.0.0.1:5000/ by default.

Access the Web Application:
![main1](https://github.com/Mayukh-Mondal-Dev/Decentralized-Document-Verifcation-System/assets/103057066/781fec20-4dab-44ed-a5e6-969455b1a3b8)


Adding a Certificate:

Click on the "Add Certificate" button.
Fill in the certificate details, such as name, email, phone number, course name, course ID, institution name, start date, and end date.
Click the "Submit" button.
The certificate data will be encrypted, added to the blockchain, and a QR code will be generated.

Viewing Certificates:

Navigate to the homepage by clicking on the "Home" button.
You will see a list of certificates in a table format, including their details, previous hash, and current hash.
Validating Certificates:

The application currently does not have a specific validation feature implemented. You can customize the validation logic in the validate_block route in app.py.
Customization:

You can customize the application by modifying the HTML templates in the templates folder or by extending its functionality as per your requirements.
Shutdown the Application:

To stop the Flask application, press Ctrl + C in the terminal where the application is running.

Cleanup:

If you want to reset the blockchain, delete the logs.db file, private_key.pem, public_key.pem, and hash.txt files in the project directory. You can also remove QR code images in the static folder if needed.

Deployment:

If you want to deploy this application to a production environment, consider using a production-ready web server, such as Gunicorn or uWSGI, and configure a reverse proxy like Nginx or Apache.



<h1>Validation Steps: </h1>
Prerequisites:

Python 3.x installed on your system.

Basic understanding of Python, Flask, SQLite, and QR code decoding.

Ensure you have the required Python packages installed. You can install them using pip:

Copy code
pip install Flask cryptography opencv-python-headless pyzbar flask-cors
Steps:

Clone the Repository:

Clone the repository to your local machine using Git:

bash
Copy code
git clone https://github.com/yourusername/certificate-validation-app.git
Replace yourusername with your actual GitHub username.

Navigate to the Project Directory:

bash
Copy code
cd certificate-validation-app
Load Private Key:

The application relies on a private key for decrypting certificate data. Ensure that the private_key.pem file is present in the project directory. If it's missing, provide your private key and save it as private_key.pem.

Run the Application:

Start the Flask application by running:

Copy code
python app.py
The application will run on the default port 5050.

Access the Web Application:
![main2](https://github.com/Mayukh-Mondal-Dev/Decentralized-Document-Verifcation-System/assets/103057066/db373f69-0bfc-47a6-9489-0465c03ed46a)


Certificate Validation:

Click on the "Choose File" button to upload a certificate image file containing a QR code.
Fill in the certificate details in the form, including course ID, course name, email, end date, institution name, name, phone number, and start date.
Click the "Submit" button.
The application will decode the QR code from the uploaded certificate image, compare the extracted data with the entered certificate details, and validate the certificate's authenticity.

Validation Result:

If the certificate data matches the decoded QR code content, the certificate is considered valid. The application will return the digital signature associated with the certificate.
If the data does not match or the certificate is not found in the database, the application will display a "not valid" message.
Customization:

You can customize the application by modifying the HTML templates in the templates folder or by extending its functionality as needed.
Deployment:

If you intend to deploy this application in a production environment, consider using a production-ready web server such as Gunicorn or uWSGI and configure a reverse proxy like Nginx or Apache.

Shutdown the Application:
To stop the Flask application, press Ctrl + C in the terminal where the application is running.

Cleanup:
If needed, you can remove uploaded certificate images from the static/uploads directory to free up storage.

