# Blockchain Certificate Verification System

A Python-based web application that uses **SHA-256 hashing** and a blockchain-inspired chain of blocks to register and verify academic certificates. It helps detect changes to certificate details by comparing their cryptographic fingerprints.

## Features

- **Certificate Registration:** Register certificate details with a unique certificate ID.
- **SHA-256 Hashing:** Generate a cryptographic fingerprint from certificate details.
- **Certificate Verification:** Check whether submitted details match the registered record.
- **Blockchain Explorer:** View blocks, certificate hashes, timestamps, and previous-hash links.
- **Duplicate Prevention:** Prevent registration of an already registered certificate ID.
- **Integrity Checking:** Perform a basic blockchain hash and link validation.
- **Responsive Interface:** Use the application through a clean web interface.

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Cryptography:** SHA-256
- **Data Format:** JSON
- **Version Control:** Git and GitHub

## Project Structure

```text
CertificateVerifier/
├── app.py
├── blockchain.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- A web browser

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/galisucharita-07/CertificateVerifier.git
```

**2. Navigate to the project directory**

```bash
cd CertificateVerifier
```

**3. Install the dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Start the application**

```bash
python app.py
```

**5. Open the application**

Visit the following URL in your browser:

http://127.0.0.1:5000

## How It Works

1. Enter a certificate ID, student name, course name, issuing organization, and issue date.
2. Register the certificate to generate its SHA-256 hash.
3. The application adds the hash to a new block linked to the previous block.
4. Submit the certificate details through the verification form.
5. The application generates a new hash and compares it with the registered fingerprint.
6. View the blockchain to inspect its blocks and run a basic integrity check.

## Example Test Cases

| Test Case | Expected Result |
|---|---|
| Register a new certificate | Registration succeeds |
| Register the same certificate ID again | Duplicate registration is rejected |
| Verify with the original details | Certificate matches the registered record |
| Change a certificate detail | Verification fails |
| Verify an unknown certificate ID | Certificate is not found |
| View the blockchain | Blocks and hash links are displayed |

## Limitations

- This is an educational prototype, not a production-ready blockchain.
- Certificate records and blocks are stored in memory and are cleared when the application restarts.
- The application uses a single local instance rather than a distributed network.
- The basic integrity check does not provide consensus, digital signatures, or protection against every form of tampering.
- Certificate authenticity depends on the reliability of the organization registering the record.

## Future Enhancements

- Add SQLite or another persistent database.
- Implement issuer authentication and digital signatures.
- Add QR-code-based certificate verification.
- Develop a Solidity smart contract and integrate it with a blockchain test network.
- Add automated unit and integration tests.
- Improve security, access control, and audit logging.

## Learning Outcomes

This project demonstrates practical knowledge of Python web development, Flask APIs, cryptographic hashing, blockchain data structures, input validation, and frontend-backend integration.

## Author

**Sucharita Gali**

GitHub: https://github.com/galisucharita-07

---

*Built as an educational project to explore blockchain concepts and certificate integrity verification.*