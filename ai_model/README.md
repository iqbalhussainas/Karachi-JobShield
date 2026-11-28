# Karachi JobShield

**Cybersecurity Awareness Center – Fake Job Advertisement Detector**

Karachi JobShield is a web-based cybersecurity awareness project designed to help users identify potential warning signs in job advertisements.

## Features

- User registration and login
- Secure password hashing
- Job advertisement text analysis
- Suspicious URL analysis
- Image-based advertisement analysis using OCR
- Tesseract OCR text extraction
- Rule-based risk scoring and risk-level assessment
- Experimental AI-based job advertisement prediction
- User-specific scan history
- Profile and password management
- CSRF protection and Content Security Policy

## Technologies Used

- Python
- Flask
- SQLite
- HTML, CSS and JavaScript
- Tesseract OCR and Pytesseract
- Scikit-learn and TF-IDF
- Logistic Regression
- Git and GitHub

## Project Structure

- `app.py` – Main Flask application
- `auth.py` – Authentication functionality
- `database.py` – Database operations
- `ai_model/` – Experimental AI model and related files
- `templates/` – HTML templates
- `static/` – CSS and static files
- `requirements.txt` – Python dependencies

## Installation

1. Clone the repository.
2. Create a Python virtual environment.
3. Activate the virtual environment.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Install Tesseract OCR.
6. Configure the required environment variables in a local `.env` file.
7. Run the application:

   `python app.py`

8. Open `http://127.0.0.1:5000` in your browser.

## Security and Testing

The project includes authentication, password hashing, CSRF protection, upload validation, user-specific scan ownership checks and HTTP security headers.

## AI Model Disclaimer

The AI component uses TF-IDF and Logistic Regression. It is experimental and was trained on an English-language dataset. Its performance on Pakistani, Urdu and Roman Urdu advertisements has not been established.

AI predictions and rule-based risk scores are indicators only. They do not prove that an advertisement is fraudulent or genuine.

## Intended Use

Karachi JobShield is an educational cybersecurity awareness project. It should not be used as the sole basis for employment or financial decisions.

## Author

Developed as a cybersecurity awareness project.