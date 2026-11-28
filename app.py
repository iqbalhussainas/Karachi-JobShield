
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)

import hashlib
import secrets
import ipaddress
import pytesseract
import os
import re

from dotenv import load_dotenv
from functools import wraps
from urllib.parse import urlparse
from PIL import Image, UnidentifiedImageError
from flask_wtf.csrf import CSRFProtect

# Tesseract OCR installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

from database import (
    create_database,
    save_scan,
    get_scan_history,
    register_user,
    get_user_id,
    delete_scan,
    get_user_profile,
    update_user_email,
    update_password_hash,
    get_dashboard_stats
)

from auth import login_user
from ai_model.predictor import predict_job_fraud


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

app = Flask(__name__)


# ==========================================
# APPLICATION SECURITY CONFIGURATION
# ==========================================

secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError(
        "SECRET_KEY is missing. Please configure it in your .env file."
    )

app.config["SECRET_KEY"] = secret_key
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
)

# Maximum uploaded file size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# Enable CSRF protection
csrf = CSRFProtect(app)

# Initialize database tables if they do not exist
create_database()


# ==========================================
# SECURITY RESPONSE HEADERS
# ==========================================

@app.after_request
def add_security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "img-src 'self' data:; "
        "style-src 'self'; "
        "script-src 'self'"
    )

    return response


# ==========================================
# FILE UPLOAD SIZE ERROR
# ==========================================

@app.errorhandler(413)
def file_too_large(error):

    flash("Image is too large. Maximum upload size is 5 MB.")

    return redirect(url_for("home"))


# ==========================================
# EMAIL VALIDATION
# ==========================================

def is_valid_email(email):

    if not isinstance(email, str):
        return False

    email = email.strip()

    if len(email) > 254 or len(email) < 6:
        return False

    if email.count("@") != 1:
        return False

    local_part, domain = email.rsplit("@", 1)

    if not local_part or len(local_part) > 64:
        return False

    if not domain or len(domain) > 253:
        return False

    local_pattern = (
        r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
        r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    )

    if not re.fullmatch(local_pattern, local_part):
        return False

    domain_pattern = (
        r"(?:[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
        r"[A-Za-z]{2,63}"
    )

    if not re.fullmatch(domain_pattern, domain):
        return False

    return True


# ==========================================
# LOGIN REQUIRED DECORATOR
# ==========================================

def login_required(route_function):

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "username" not in session or "user_id" not in session:
            session.clear()
            flash("Please login first to access this page.")
            return redirect(url_for("login"))

        return route_function(*args, **kwargs)

    return wrapper


# ==========================================
# PASSWORD HASHING
# ==========================================

def generate_password_hash(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000
    ).hex()

    return salt.hex() + "$" + password_hash


# ==========================================
# JOB ADVERTISEMENT ANALYSIS
# ==========================================

def analyze_job_ad_text(job_ad):

    warnings = []
    risk_score = 0
    text = job_ad.lower()

    # Detect payment requests
    payment_keywords = [
        "registration fee",
        "advance payment",
        "processing fee",
        "security deposit",
        "pay to apply",
        "pay before joining",
        "training fee"
    ]

    payment_detected = False

    # Split advertisement into sentences
    sentences = re.split(r"[.!?\n]", text)

    negative_patterns = [
        r"\bno\s+(?:registration|advance|processing|security|training|application)?\s*(?:fee|fees|payment|deposit|charge)s?\b",

        r"\b(?:registration|advance|processing|security|training|application)?\s*(?:fee|fees|payment|deposit|charge)s?\s+(?:is|are)\s+not\s+required\b",

        r"\b(?:does not|do not|don't|never)\s+(?:charge|require|ask for|request)\s+(?:(?:a|any)\s+)?(?:registration|advance|processing|security|training|application)?\s*(?:fee|fees|payment|deposit|charge)s?\b",

        r"\b(?:do not|don't|never)\s+pay\s+(?:any\s+)?(?:registration|advance|processing|security|training|application)?\s*(?:fee|fees|payment|deposit|charge)s?\b",

        r"\bno payment\s+(?:is\s+)?required\b",
        r"\bnot required to pay\b"
    ]

    for keyword in payment_keywords:

        for sentence in sentences:

            if keyword in sentence:

                is_negative = any(
                    re.search(pattern, sentence)
                    for pattern in negative_patterns
                )

                if not is_negative:
                    payment_detected = True
                    break

        if payment_detected:
            break

    if payment_detected:
        risk_score += 30
        warnings.append(
            "The advertisement asks for registration or advance payment."
        )


    # Other job advertisement risk rules
    risk_rules = [

        (20, [
            "no interview",
            "without interview",
            "without an interview",
            "interview not required",
            "no interview needed"
        ], "The advertisement says no interview is required."),

        (20, [
            "guaranteed job",
            "guaranteed employment",
            "100% job guarantee",
            "sure job"
        ], "The advertisement promises guaranteed employment."),

        (15, [
            "urgent hiring",
            "apply immediately",
            "limited seats",
            "apply today"
        ], "The advertisement uses urgent hiring pressure."),

        (15, [
            "earn millions",
            "easy money",
            "get rich quickly",
            "high income with no work",
            "earn thousands daily"
        ], "The advertisement makes unrealistic earning promises."),

        (30, [
            "share your otp",
            "send your otp",
            "share your pin",
            "send your atm pin",
            "share your password",
            "bank password"
        ], "The advertisement requests sensitive banking or account credentials.")
    ]

    for points, keywords, warning in risk_rules:

        if any(keyword in text for keyword in keywords):
            risk_score += points
            warnings.append(warning)

    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        risk_level = "High Risk"

    elif risk_score >= 30:
        risk_level = "Medium Risk"

    else:
        risk_level = "Low Risk"

    if not warnings:
        warnings.append(
            "No warning signs detected by our basic rules."
        )

    return risk_score, risk_level, warnings


# ==========================================
# JOB LINK ANALYSIS HELPER
# ==========================================

def analyze_job_link(link):

    warnings = []
    risk_score = 0

    link = link.strip()

    if not link:
        return 0, "Invalid Link", ["Please enter a job link."]

    if "://" not in link:
        link = "https://" + link

    try:

        parsed = urlparse(link)
        hostname = parsed.hostname

        if parsed.scheme not in ("http", "https") or not hostname:
            return 0, "Invalid Link", [
                "The URL format or protocol is invalid."
            ]

        # Check IP address
        try:

            ipaddress.ip_address(hostname)

            risk_score += 30

            warnings.append(
                "The link uses an IP address instead of a normal domain name."
            )

        except ValueError:
            pass

        # Check URL shorteners
        shorteners = [
            "bit.ly",
            "tinyurl.com",
            "t.co",
            "is.gd",
            "cutt.ly",
            "shorturl.at"
        ]

        if hostname.lower() in shorteners:

            risk_score += 25

            warnings.append(
                "The link uses a URL shortening service that hides its destination."
            )

        # Check HTTP
        if parsed.scheme == "http":

            risk_score += 15

            warnings.append(
                "The link uses HTTP instead of HTTPS."
            )

        # Check suspicious words
        suspicious_words = [
            "verify-account",
            "account-verification",
            "urgent-payment",
            "job-registration",
            "free-money",
            "claim-prize",
            "password-reset"
        ]

        address_text = hostname.lower() + parsed.path.lower()

        if any(word in address_text for word in suspicious_words):

            risk_score += 15

            warnings.append(
                "The URL contains suspicious words often associated with phishing."
            )

        # Check @ symbol
        if "@" in parsed.netloc:

            risk_score += 25

            warnings.append(
                "The URL contains an @ symbol that may hide the actual destination."
            )

        # Check encoded domain names
        if "xn--" in hostname.lower():

            risk_score += 20

            warnings.append(
                "The domain contains encoded characters that may imitate another website."
            )

        risk_score = min(risk_score, 100)

        if risk_score >= 60:
            risk_level = "High Risk"

        elif risk_score >= 30:
            risk_level = "Medium Risk"

        else:
            risk_level = "Low Risk"

        if not warnings:
            warnings.append(
                "No suspicious URL patterns were detected by these basic checks."
            )

        return risk_score, risk_level, warnings

    except (ValueError, UnicodeError):

        return 0, "Invalid Link", [
            "The URL could not be analyzed. Please check its format."
        ]


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# JOB ADVERTISEMENT ANALYSIS ROUTE
# ==========================================

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():

    job_ad = request.form.get("job_ad", "").strip()

    if not job_ad:

        flash("Please enter a job advertisement.")

        return redirect(url_for("home"))

    if len(job_ad) > 20000:

        flash(
            "Advertisement is too long. Maximum length is 20,000 characters."
        )

        return redirect(url_for("home"))

    # Existing rule-based analysis
    risk_score, risk_level, warnings = analyze_job_ad_text(job_ad)

    # Experimental AI prediction
    try:

        ai_prediction = predict_job_fraud(job_ad)

        ai_prediction_label = (
            "Fraudulent" if ai_prediction == 1 else "Genuine"
        )

    except Exception:

        app.logger.exception("AI MODEL PREDICTION ERROR")

        ai_prediction_label = "AI Unavailable"

    # Save original rule-based result
    save_scan(
        job_ad,
        risk_score,
        risk_level,
        session["user_id"]
    )

    return render_template(
        "result.html",
        job_ad=job_ad,
        risk_score=risk_score,
        risk_level=risk_level,
        warnings=warnings,
        ai_prediction_label=ai_prediction_label
    )


# ==========================================
# JOB LINK ANALYSIS ROUTE
# ==========================================

@app.route("/check_link", methods=["GET", "POST"])
@login_required
def check_link():

    if request.method == "POST":

        job_link = request.form.get("job_link", "").strip()

        if not job_link:
            flash("Please enter a job link.")
            return redirect(url_for("check_link"))

        if len(job_link) > 2048:
            flash("The link is too long.")
            return redirect(url_for("check_link"))

        risk_score, risk_level, warnings = analyze_job_link(job_link)

        save_scan(
            job_link,
            risk_score,
            risk_level,
            session["user_id"]
        )

        return render_template(
            "link_result.html",
            job_link=job_link,
            risk_score=risk_score,
            risk_level=risk_level,
            warnings=warnings
        )

    return render_template("check_link.html")


# ==========================================
# USER DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    stats = get_dashboard_stats(session["user_id"])

    return render_template(
        "dashboard.html",
        stats=stats
    )


# ==========================================
# USER SCAN HISTORY
# ==========================================

@app.route("/history")
@login_required
def history():

    scans = get_scan_history(session["user_id"])

    return render_template(
        "history.html",
        scans=scans
    )


# ==========================================
# USER REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:

            flash("Please complete all required fields.")

            return redirect(url_for("register"))

        if not is_valid_email(email):

            flash("Please enter a valid email address.")

            return redirect(url_for("register"))

        if password != confirm_password:

            flash("Passwords do not match!")

            return redirect(url_for("register"))

        if len(password) < 8:

            flash("Password must be at least 8 characters.")

            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        result = register_user(
            username,
            email,
            password_hash
        )

        if result:

            flash("Registration successful! Please login.")

            return redirect(url_for("login"))

        flash("Username or email already exists!")

        return redirect(url_for("register"))

    return render_template("register.html")


# ==========================================
# USER LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if login_user(username, password):

            user_id = get_user_id(username)

            if user_id is not None:

                session.clear()

                session["username"] = username
                session["user_id"] = user_id

                flash("Login successful!")

                return redirect(url_for("home"))

        flash("Invalid username or password!")

    return render_template("login.html")


# ==========================================
# USER LOGOUT
# ==========================================

@app.route("/logout", methods=["POST"])
@login_required
def logout():

    session.clear()

    flash("You have logged out successfully.")

    return redirect(url_for("home"))


# ==========================================
# USER PROFILE
# ==========================================

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    user_id = session["user_id"]

    if request.method == "POST":

        action = request.form.get("action")

        # Update email
        if action == "update_email":

            new_email = request.form.get("email", "").strip()

            if not is_valid_email(new_email):

                flash("Please enter a valid email address.")

                return redirect(url_for("profile"))

            result = update_user_email(
                user_id,
                new_email
            )

            if result:
                flash("Email updated successfully!")

            else:
                flash("This email may already be registered.")

            return redirect(url_for("profile"))

        # Change password
        elif action == "change_password":

            current_password = request.form.get(
                "current_password", ""
            )

            new_password = request.form.get(
                "new_password", ""
            )

            confirm_password = request.form.get(
                "confirm_password", ""
            )

            if not current_password or not new_password or not confirm_password:

                flash("Please complete all password fields.")

                return redirect(url_for("profile"))

            if not login_user(session["username"], current_password):

                flash("Current password is incorrect.")

                return redirect(url_for("profile"))

            if len(new_password) < 8:

                flash("New password must be at least 8 characters.")

                return redirect(url_for("profile"))

            if new_password != confirm_password:

                flash("New passwords do not match.")

                return redirect(url_for("profile"))

            new_hash = generate_password_hash(new_password)

            result = update_password_hash(
                user_id,
                new_hash
            )

            if result:
                flash("Password changed successfully!")

            else:
                flash("Password could not be changed.")

            return redirect(url_for("profile"))

    user = get_user_profile(user_id)

    if user is None:

        session.clear()

        flash("User profile not found. Please login again.")

        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        user=user
    )


# ==========================================
# IMAGE OCR DETECTOR
# ==========================================

@app.route("/check_image", methods=["GET", "POST"])
@login_required
def check_image():

    if request.method == "GET":

        return redirect(url_for("home"))

    uploaded_image = request.files.get("job_image")

    if uploaded_image is None or not uploaded_image.filename:

        flash("Please select a job advertisement image.")

        return redirect(url_for("home"))

    allowed_extensions = {"png", "jpg", "jpeg"}

    extension = uploaded_image.filename.rsplit(".", 1)[-1].lower()

    if "." not in uploaded_image.filename or extension not in allowed_extensions:

        flash("Only PNG, JPG and JPEG images are allowed.")

        return redirect(url_for("home"))

    try:

        uploaded_image.stream.seek(0)

        # Validate uploaded image
        with Image.open(uploaded_image.stream) as image:

            if image.format not in ("PNG", "JPEG"):

                flash("The uploaded file is not a supported image.")

                return redirect(url_for("home"))

            width, height = image.size

            if width <= 0 or height <= 0 or width * height > 20_000_000:

                flash("The image dimensions are too large.")

                return redirect(url_for("home"))

            image.verify()

        # Reopen image after verification
        uploaded_image.stream.seek(0)

        with Image.open(uploaded_image.stream) as image:

            image = image.convert("RGB")

            # Extract text using Tesseract OCR
            extracted_text = pytesseract.image_to_string(image)

        extracted_text = extracted_text.strip()

        if not extracted_text:

            flash(
                "No readable text was found. Please try a clearer job poster."
            )

            return redirect(url_for("home"))

        # Limit extracted text
        extracted_text = extracted_text[:20000]

        # Existing rule-based analysis
        risk_score, risk_level, warnings = analyze_job_ad_text(
            extracted_text
        )

        # Experimental AI prediction
        try:

            ai_prediction = predict_job_fraud(extracted_text)

            ai_prediction_label = (
                "Fraudulent" if ai_prediction == 1 else "Genuine"
            )

        except Exception:

            app.logger.exception("AI MODEL PREDICTION ERROR")

            ai_prediction_label = "AI Unavailable"

        # Save original rule-based result
        save_scan(
            extracted_text,
            risk_score,
            risk_level,
            session["user_id"]
        )

        return render_template(
            "image_result.html",
            extracted_text=extracted_text,
            risk_score=risk_score,
            risk_level=risk_level,
            warnings=warnings,
            ai_prediction_label=ai_prediction_label
        )

    except (
        UnidentifiedImageError,
        OSError,
        Image.DecompressionBombError
    ):

        app.logger.exception("IMAGE PROCESSING ERROR")

        flash(
            "The image could not be processed. Please upload a valid image."
        )

        return redirect(url_for("home"))

    except pytesseract.TesseractNotFoundError:

        app.logger.exception("TESSERACT NOT FOUND")

        flash(
            "Tesseract OCR was not found. Please check its installation."
        )

        return redirect(url_for("home"))

    except pytesseract.TesseractError:

        app.logger.exception("OCR PROCESSING ERROR")

        flash(
            "OCR processing failed. Please try another image."
        )

        return redirect(url_for("home"))


# ==========================================
# DELETE SCAN
# ==========================================

@app.route("/delete_scan/<int:scan_id>", methods=["POST"])
@login_required
def delete_scan_route(scan_id):

    result = delete_scan(
        scan_id,
        session["user_id"]
    )

    if result:

        flash("Scan deleted successfully.")

    else:

        flash(
            "Scan not found or you do not have permission to delete it."
        )

    return redirect(url_for("history"))


# ==========================================
# CYBERSECURITY AWARENESS
# ==========================================

@app.route("/tips")
def tips():

    return render_template("tips.html")


# ==========================================
# APPLICATION START
# ==========================================

if __name__ == "__main__":

    app.run(debug=False)
