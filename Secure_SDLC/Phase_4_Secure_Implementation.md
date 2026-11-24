\# Karachi JobShield

\## Secure SDLC – Phase 4: Secure Implementation



\### 1. Introduction



This phase describes how the security requirements and secure architecture of Karachi JobShield were implemented in the application.



The project uses Python, Flask, SQLite, HTML, CSS, Pillow and Tesseract OCR.



\### 2. Secure Authentication Implementation



\- User registration and login functionality were implemented.

\- Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes.

\- Password hashing uses 600,000 iterations.

\- Password verification uses a secure comparison function.

\- Database queries use parameterized SQL statements.

\- Protected routes require authentication.



\### 3. Authorization and Access Control



\- User scan records are associated with individual user IDs.

\- Dashboard statistics display user-specific information.

\- Scan history is filtered by the authenticated user's ID.

\- Scan deletion checks both the scan ID and the user's ID.

\- Users cannot access another user's scan records through normal application routes.



\### 4. Input and Database Security



\- User inputs are processed through application validation.

\- Parameterized SQL queries are used to reduce SQL injection risks.

\- Jinja template output escaping helps prevent stored and reflected XSS.

\- Application errors are handled without intentionally exposing sensitive database details.



\### 5. CSRF Protection



Flask-WTF CSRF protection is used to protect supported form submissions against Cross-Site Request Forgery.



Forms include CSRF tokens, and invalid or missing tokens are rejected.



\### 6. Secure File Upload Implementation



The image analysis feature includes:



\- PNG, JPG and JPEG extension restrictions.

\- Maximum upload size of 5 MB.

\- Actual image format verification using Pillow.

\- Image dimension restrictions.

\- Handling of invalid and unreadable images.

\- OCR text extraction using Tesseract.

\- Error handling for image processing and OCR failures.



\### 7. Session and Security Header Configuration



The application uses an environment-configured Flask secret key.



The following response security headers are configured:



\- X-Content-Type-Options: nosniff

\- X-Frame-Options: DENY

\- Referrer-Policy: strict-origin-when-cross-origin

\- Permissions-Policy

\- Content-Security-Policy



Flask debug mode is disabled in the application configuration.



\### 8. Security Implementation Review



The implementation was reviewed for authentication, authorization, password storage, database access, CSRF protection, image upload validation, session handling and security headers.



\### 9. Remaining Security Improvements



The following improvements should be considered before production deployment:



\- Implement login rate limiting.

\- Deploy using HTTPS.

\- Enable secure cookie settings when using HTTPS.

\- Perform additional penetration testing.

\- Review and update dependencies regularly.

\- Consider external threat-intelligence integration for URL analysis.



\### 10. Conclusion



Karachi JobShield implements several important security controls across authentication, authorization, database access, file uploads, sessions and HTTP response headers.



The implementation provides a foundation for secure application operation. Additional security testing and production hardening remain necessary.
