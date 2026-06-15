// vaccine_certificate.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COVID-19 Vaccination Certificate</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <script src="generate_certificate.js" defer></script>
</head>
<body>
    <div class="certificate-container" id="certificate">
        <!-- Government Header -->
        <div class="header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Coat_of_arms_of_the_United_States.svg/320px-Coat_of_arms_of_the_United_States.svg.png" alt="Government Seal" class="logo">
            <h1>Department of Health & Human Services</h1>
            <h2>COVID-19 Vaccination Record Card</h2>
        </div>

        <!-- Personal Information Section -->
        <div class="section">
            <h3>Personal Information</h3>
            <div class="field">
                <label>Full Name:</label>
                <span id="fullName">John Doe</span>
            </div>
            <div class="field">
                <label>Date of Birth:</label>
                <span id="dob">01/15/1985</span>
            </div>
            <div class="field">
                <label>Patient ID/Passport:</label>
                <span id="patientId">USA123456789</span>
            </div>
        </div>

        <!-- Vaccination Details -->
        <div class="section">
            <h3>Vaccination Details</h3>
            <div class="field">
                <label>Manufacturer:</label>
                <span id="manufacturer">Pfizer-BioNTech</span>
            </div>
            <div class="field">
                <label>Lot Number:</label>
                <span id="lotNumber">EL3242</span>
            </div>
            <div class="field">
                <label>Dose 1 Date:</label>
                <span id="dose1Date">04/15/2021</span>
            </div>
            <div class="field">
                <label>Dose 2 Date:</label>
                <span id="dose2Date">05/06/2021</span>
            </div>
            <div class="field">
                <label>Healthcare Provider:</label>
                <span id="provider">City Medical Center</span>
            </div>
        </div>

        <!-- QR Code Section -->
        <div class="qr-section">
            <div id="qrcode"></div>
            <p>Scan to verify at <em>verify.covid19-dhhs.gov/check</em></p>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>This certificate is an official record of COVID-19 vaccination.</p>
            <p class="small">Issued by: U.S. Department of Health & Human Services</p>
        </div>
    </div>

    <!-- Form for Editing -->
    <div class="edit-form">
        <h3>Edit Certificate Data</h3>
        <input type="text" id="inputName" placeholder="Full Name" value="John Doe">
        <input type="text" id="inputDob" placeholder="Date of Birth" value="01/15/1985">
        <input type="text" id="inputManufacturer" placeholder="Vaccine Manufacturer" value="Pfizer-BioNTech">
        <button onclick="updateCertificate()">Update Certificate</button>
        <button onclick="downloadPDF()">Download as PDF</button>
    </div>
</body>
</html>