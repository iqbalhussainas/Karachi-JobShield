# Karachi JobShield
## Secure SDLC – Phase 1: Planning and Requirements

### 1. Project Overview

Karachi JobShield is a cybersecurity awareness and job scam detection web application developed using Python, Flask, and SQLite.

The system helps users identify potentially suspicious job advertisements, recruitment links, and job poster images.

### 2. Project Objectives

- Identify suspicious job advertisement content.
- Detect potentially risky recruitment URLs.
- Extract text from job poster images using OCR.
- Educate users about online job scams.
- Protect user accounts and personal information.
- Maintain secure and private scan history.

### 3. Project Scope

The project includes:

1. Job Advertisement Analyzer
2. Suspicious Job Link Detector
3. Job Poster OCR Detector
4. User Registration and Login
5. User Dashboard and Profile
6. Scan History Management
7. Cybersecurity Awareness Center

### 4. Project Technologies

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Flask | Web application framework |
| SQLite | Database |
| HTML and CSS | Frontend |
| Pillow | Image processing |
| Tesseract OCR | Text extraction from images |
| Git and GitHub | Version control |

### 5. Intended Users

- Job seekers
- Students
- Fresh graduates
- People searching for online employment opportunities

### 6. Security Objectives

- Protect user passwords using secure password hashing.
- Prevent unauthorized access to user accounts and records.
- Validate all user inputs.
- Protect the database against SQL injection.
- Validate uploaded images and restrict file sizes.
- Protect application sessions.
- Prevent common web application vulnerabilities.
- Maintain user privacy and data confidentiality.

### 7. Project Limitations

Karachi JobShield uses rule-based analysis and does not guarantee that a job advertisement or website is genuine or fraudulent.

The link detector does not currently check live threat-intelligence databases. OCR may also extract text incorrectly from unclear or decorative images.

### 8. Secure SDLC Commitment

Security will be considered throughout the software development lifecycle, including planning, requirements analysis, design, implementation, testing, deployment, and maintenance.

Every new feature must be reviewed and tested for security before being considered complete.
