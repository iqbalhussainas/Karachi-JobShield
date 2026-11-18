# Karachi JobShield
## Secure SDLC – Phase 3: Secure System Design

### 1. System Architecture

Karachi JobShield follows a web application architecture.

The main components are:

1. User Interface – HTML and CSS.
2. Application Layer – Python and Flask.
3. Authentication Layer – Registration, login and session management.
4. Detection Layer – Job advertisement analysis, URL analysis and OCR.
5. Database Layer – SQLite.
6. Image Processing Layer – Pillow and Tesseract OCR.

### 2. Application Data Flow

User
↓
Web Interface
↓
Flask Routes
↓
Authentication and Authorization
↓
Input Validation
↓
Detection Functions
↓
Database (where required)
↓
Analysis Results
↓
User Interface

### 3. Security Controls in the Architecture

| Component | Planned security control |
|---|---|
| Web Interface | Safe output escaping |
| Flask Routes | Authentication and authorization |
| Input Validation | Validate and restrict user input |
| Database | Parameterized SQL queries |
| Password Storage | Salted password hashing |
| Session Management | Secure cookie configuration |
| Image Upload | File validation and size limits |
| OCR Processing | Image dimension and resource limits |
| Error Handling | Avoid exposing sensitive information |

### 4. Authentication Design

Users must authenticate before accessing protected features.

Passwords must be hashed before database storage. The application must verify passwords using the secure password verification process.

### 5. Database Design

The database stores user account information and scan history.

User-specific scan records must be associated with the correct user ID. Every request to view, update, or delete a record must verify ownership.

### 6. Secure File Upload Design

Uploaded images must be validated before OCR processing.

The application must restrict accepted image formats, file size and image dimensions. Images should be processed in memory rather than stored unnecessarily.

### 7. Security Design Principles

- Least Privilege
- Defense in Depth
- Input Validation
- Secure Defaults
- Separation of Responsibilities
- Fail Securely
- Privacy by Design

### 8. Conclusion

The secure architecture defines how Karachi JobShield components interact and where security controls should be applied. These design decisions will guide the implementation and security testing phases.