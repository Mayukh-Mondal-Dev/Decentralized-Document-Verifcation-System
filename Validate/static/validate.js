const uploadButton = document.querySelector(".btn-submit");
const uploadFeedback = document.querySelector("#upload-feedback");

uploadButton.addEventListener("click", function () {
  uploadFeedback.textContent = "Uploading..."; // Display uploading message
  setTimeout(function () {
    uploadFeedback.textContent = "File Uploaded!"; // Display upload success message (you can customize this)
  }, 2000); // Simulate a 2-second upload process (you can adjust this time)
});

document.getElementById("registration-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  // Retrieve and display form values (excluding the file input)
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const contact = document.getElementById("contact").value;
  const courseName = document.getElementById("courseName").value;
  const courseId = document.getElementById("courseId").value;
  const instituteName = document.getElementById("instituteName").value;
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  const fileInput = document.getElementById("file");

  // Check if a file is selected
  if (fileInput.files.length === 0) {
    alert("Please select a PDF file for upload.");
    return;
  }

  console.log("certificate uploaded: ", fileInput.files[0]);

  const formData = new FormData();

  formData.append("name", name);
  formData.append("email", email);
  formData.append("phnumber", contact);
  formData.append("coursename", courseName);
  formData.append("courseid", courseId);
  formData.append("instname", instituteName);
  formData.append("startdate", startDate);
  formData.append("enddate", endDate);
  formData.append("certificate", fileInput.files[0]);

  const res = await fetch("http://127.0.0.1:5050", {
    method: "POST",
    body: formData,
  });

  if (res.status === 200) {
    const { signature } = await res.json();
    console.log(signature);

    const certificateCanvas = document.getElementById("certificateCanvas");
    const certificateContext = certificateCanvas.getContext("2d");

    const templateImage = new Image();
    templateImage.src = URL.createObjectURL(fileInput.files[0]);
    templateImage.onload = function () {
      certificateCanvas.width = templateImage.width;
      certificateCanvas.height = templateImage.height;

      certificateContext.drawImage(templateImage, 0, 0);
      certificateContext.font = "bold 20px Arial";
      certificateContext.fillStyle = "white";
      certificateContext.fillText(signature, 120, 1300);

      // Here we convert canvas to data URL (PNG)
      const certificateDataURL = certificateCanvas.toDataURL("image/png");

      // Here we set the download link href
      const certificateLink = document.getElementById("downloadLink");
      certificateLink.href = certificateDataURL;
      certificateLink.style.display = "block";
      certificateLink.click();
    };
  } else if (res.status === 400) {
    // Handle the "not valid" response here
    uploadFeedback.textContent = "Validation failed. Certificate is not valid.";
  } else {
    // Handle other response statuses if needed
    uploadFeedback.textContent = "An error occurred during validation.";
  }
});
