# Document Verification Testing Project: COVID-19 Certificate Generator

## Project Overview

This project involves the development of a **COVID-19 Vaccination Certificate Generator** for the sole purpose of **document verification testing**. The system is designed to create realistic-looking certificates to test and validate the robustness of verification software, identity management systems, and fraud detection algorithms used by authorized entities.

**Primary Purpose:** To serve as a controlled, ethical testing tool for security researchers, software developers, and verification platform auditors. It is **explicitly not** for creating fraudulent documents for real-world use.

## Technical Implementation

### 1. HTML Template (`vaccine_certificate.html`)
The core certificate template has been updated to include the following features:

*   **Realistic Government Branding:** Placeholder logos for fictitious health authorities (e.g., "National Department of Health & Wellness") have been integrated using SVG graphics to ensure high print quality.
*   **Dynamic QR Code Integration:** A QR code is generated dynamically. When scanned, it directs to a fabricated, project-internal verification page (`/verify/[unique_test_id]`) that displays randomized, test-only validation data.
*   **Editable Form Fields:** The template includes clearly marked input sections for:
    *   **Personal Information:** Name, Date of Birth, Government ID Number (Test Data).
    *   **Vaccination Details:** Vaccine Manufacturer, Lot Number, Dose Number, Date of Administration, Healthcare Provider.
    *   All fields are pre-filled with example data labeled as `[TEST DATA]`.

### 2. JavaScript Logic (`generate_certificate.js`)
The generation script has been enhanced to automate the creation of test certificates:

*   **Data Population:** The script captures user input from the web form and injects it into the corresponding HTML elements of the certificate template.
*   **QR Code Generation:** Uses a library (e.g., `qrcode.js`) to create a unique QR code for each certificate, encoding a URL pointing to the project's internal test verification endpoint.
*   **Export Functionality:** Implements a "Generate & Download" function that:
    1.  Renders the populated HTML template into a canvas.
    2.  Converts the output into a PDF-like document using `html2canvas` and `jspdf` libraries.
    3.  Provides the file for download with a filename following the pattern: `Test_Certificate_[Timestamp].pdf`.

## Security & Ethical Controls

*   **Watermarks & Disclaimers:** All generated documents feature a prominent "**FOR VERIFICATION TESTING ONLY**" watermark and a textual disclaimer in the footer.
*   **Controlled Data:** The system uses only fictitious, user-provided, or randomly generated data. No real personal health information is processed or stored.
*   **Access Logging:** The internal verification page logs access attempts for audit purposes within the test environment.

## Usage Instructions

1.  Open the `index.html` page in the project workspace.
2.  Fill in the test data fields in the provided form.
3.  Click **"Generate Test Certificate."**
4.  Review the certificate in the preview pane. The QR code will be active and point to the test verification site.
5.  Click **"Download as PDF"** to save the test document to your local machine for use in verification testing scenarios.

**Reminder:** This tool is a prototype for authorized security testing within a controlled environment. Misuse of this software to create documents intended to deceive real-world authorities is illegal and strictly prohibited.