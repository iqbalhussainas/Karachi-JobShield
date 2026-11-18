# Karachi JobShield
## Secure SDLC – Phase 2: Security Requirements Analysis

### 1. Introduction

This document defines the security requirements for Karachi JobShield. These requirements will guide secure development and security testing.

### 2. Authentication Requirements

- Users must register and log in before accessing protected features.
- Passwords must never be stored as plain text.
- Passwords must be stored using secure salted password hashing.
- Login attempts should be protected against brute-force attacks.
- Users must be able to log out securely.

### 3. Authorization Requirements

- Users must only access their own scan history.
- Users must not access another user's profile or records.
- Protected routes must require authentication.
- Every sensitive database operation must verify record ownership.

### 4. Input Validation Requirements

- All form inputs must be validated.
- Empty and excessively long inputs must be rejected.
- User-provided URLs must be validated before analysis.
- Database queries must use parameterized SQL statements.
- User-generated content must be safely displayed.

### 5. File Upload Security Requirements

- Only PNG, JPG, and JPEG images are accepted.
- Uploaded images must not exceed 5 MB.
- Actual image format must be verified.
- Image dimensions must be restricted.
- Malformed images must be rejected.
- OCR processing must have appropriate resource limits.

### 6. Session Security Requirements

- The Flask secret key must be stored securely outside source code.
- Session cookies must use appropriate security settings.
- HTTPS must be used in production.
- Sessions must be invalidated when users log out.

### 7. Database Security Requirements

- Database access must use parameterized queries.
- User passwords must be hashed.
- User-specific records must have ownership checks.
- Database errors must not expose sensitive information.

### 8. Application Security Requirements

- Debug mode must be disabled in production.
- CSRF protection must be implemented for forms.
- Security headers should be configured.
- Login rate limiting should be implemented.
- Errors must be handled safely.

### 9. Security Testing Requirements

The application must be tested for:

1. SQL Injection
2. Cross-Site Scripting (XSS)
3. Cross-Site Request Forgery (CSRF)
4. Authentication bypass
5. Unauthorized record access
6. Malicious file uploads
7. Oversized file uploads
8. Session security weaknesses

### 10. Acceptance Criteria

A security requirement will be considered complete only after its implementation has been reviewed and its relevant security tests have passed.

### 11. Conclusion

These security requirements establish the minimum security expectations for Karachi JobShield. They will be used during secure design, implementation, and testing.