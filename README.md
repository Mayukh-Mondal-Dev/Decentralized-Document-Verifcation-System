# Decentralized-Document-Verifcation-System
<h1>Flask Blockchain Application</h1>
The project is a web-based certificate generation and validation system using Flask. It encrypts user-submitted certificate data, stores it in a blockchain, and generates a QR code for verification. The validation component decrypts data, checks it against the blockchain, and confirms certificate authenticity.
This README provides step-by-step instructions on setting up and running a Flask-based blockchain web application for creating and validating digital certificates. The application allows you to add certificate information, encrypt it, and store it in a blockchain. It also generates QR codes for each certificate for easy retrieval and validation.

<h3>Prerequisites:</h3>

Python 3.x installed on your system.

Basic understanding of Python, Flask, and SQLite.

Ensure you have the required Python packages installed. You can install them using pip:

The application uses public-key cryptography for encryption. It generates key pairs for encryption and stores them in private_key.pem and public_key.pem files. Run the following command to generate the keys:


Access the Web Application:

![main1](https://github.com/Mayukh-Mondal-Dev/Decentralized-Document-Verifcation-System/assets/103057066/781fec20-4dab-44ed-a5e6-969455b1a3b8)


<h3>Adding a Certificate:</h3>

Click on the "Add Certificate" button.
Fill in the certificate details, such as name, email, phone number, course name, course ID, institution name, start date, and end date.
Click the "Submit" button.
The certificate data will be encrypted, added to the blockchain, and a QR code will be generated.

<h3>Viewing Certificates:</h3>

Navigate to the homepage by clicking on the "Home" button.
You will see a list of certificates in a table format, including their details, previous hash, and current hash.
Validating Certificates:

The application currently does not have a specific validation feature implemented. You can customize the validation logic in the validate_block route in app.py.



<h1>Validation Steps: </h1>
Prerequisites:

Python 3.x installed on your system.

Basic understanding of Python, Flask, SQLite, and QR code decoding.

Ensure you have the required Python packages installed. You can install them using pip:

The application relies on a private key for decrypting certificate data. Ensure that the private_key.pem file is present in the project directory. If it's missing, provide your private key and save it as private_key.pem.

Access the Web Application:

![main2](https://github.com/Mayukh-Mondal-Dev/Decentralized-Document-Verifcation-System/assets/103057066/db373f69-0bfc-47a6-9489-0465c03ed46a)


<h3>Certificate Validation:</h3>

Click on the "Choose File" button to upload a certificate image file containing a QR code.
Fill in the certificate details in the form, including course ID, course name, email, end date, institution name, name, phone number, and start date.
Click the "Submit" button.
The application will decode the QR code from the uploaded certificate image, compare the extracted data with the entered certificate details, and validate the certificate's authenticity.

<h3>Validation Result:</h3>

If the certificate data matches the decoded QR code content, the certificate is considered valid. The application will return the digital signature associated with the certificate.
If the data does not match or the certificate is not found in the database, the application will display a "not valid" message.

