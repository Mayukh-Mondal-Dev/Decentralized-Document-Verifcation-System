let generated_qr_code;
async function uploadCertificateInfo() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phnumber = document.getElementById("phnumber").value;
    const coursename = document.getElementById("coursename").value;
    const courseid = document.getElementById("courseid").value;
    const instname = document.getElementById("instname").value;
    const startdate = document.getElementById("startdate").value;
    const enddate = document.getElementById("enddate").value;

    const formData = new FormData();

    formData.append("name", name);
    formData.append("email", email);
    formData.append("phnumber", phnumber);
    formData.append("coursename", coursename);
    formData.append("courseid", courseid);
    formData.append("instname", instname);
    formData.append("startdate", startdate);
    formData.append("enddate", enddate);

    console.log("uploading certificate data: ", {
        name, email, phnumber, coursename, courseid, instname, startdate, enddate
    });
    const res = await fetch('http://127.0.0.1:5000/add_block', {
        method: "POST",
        body: formData
    })
    const { qr_code } = await res.json();
    generated_qr_code = `/static/${qr_code}`
    console.log(generated_qr_code);
}

async function generateCertificate() {
    const name = document.getElementById("name").value;
    const coursename = document.getElementById("coursename").value;
    const courseid = document.getElementById("courseid").value;
    const instname = document.getElementById("instname").value;
    const startdate = document.getElementById("startdate").value;
    const enddate = document.getElementById("enddate").value;

    if (!name) {
        alert("Please enter a name.");
        return;
    }

    await uploadCertificateInfo();

    const certificateCanvas = document.getElementById("certificateCanvas");
    const certificateContext = certificateCanvas.getContext("2d");

    // Here we load the certificate template as an image
    const templateImage = new Image();
    templateImage.src = "/static/certificate_template.png"; // Use certificate template image here

    console.log("downloading certificate: ", generated_qr_code);
    const generated_qr_code_img = new Image()
    generated_qr_code_img.crossOrigin = "anonymous"
    generated_qr_code_img.src = generated_qr_code;

    templateImage.onload = function () {
        // Here we set canvas dimensions to match the template image
        certificateCanvas.width = templateImage.width;
        certificateCanvas.height = templateImage.height;

        // Here we draw the template image on the canvas
        certificateContext.drawImage(templateImage, 0, 0);

        // Here we customize the certificate by adding the user's name
        certificateContext.font = "bold 80px Arial";
        certificateContext.fillStyle = "white";
        certificateContext.fillText(name, 190, 480); // Adjust position here

        // Here we customize the certificate by adding the course name
        certificateContext.font = "bold 50px Arial";
        certificateContext.fillText(coursename, 210, 665);

        // Here we customize the certificate by adding the course id
        certificateContext.font = "bold 50px Arial";
        certificateContext.fillText(courseid, 550, 734);

        // Here we customize the certificate by adding the institution name and location
        certificateContext.font = "bold 50px Arial";
        certificateContext.fillText(instname, 210, 860);

        // Here we customize the certificate by adding the course start date
        certificateContext.font = "bold 50px Arial";
        certificateContext.fillText(startdate, 400, 935);

        // Here we customize the certificate by adding the course end date
        certificateContext.font = "bold 50px Arial";
        certificateContext.fillText(enddate, 850, 935);

        certificateContext.drawImage(generated_qr_code_img, 1590, 1020, 250, 250);

        // Here we convert canvas to data URL (PNG)
        const certificateDataURL = certificateCanvas.toDataURL("image/png");

        // Here we set the download link href
        const certificateLink = document.getElementById("downloadLink");
        certificateLink.href = certificateDataURL;
        certificateLink.style.display = "block";
    };
}