# Karachi JobShield
## Threat Modeling

### 1. Purpose

Threat modeling identifies possible security threats against Karachi JobShield and defines controls to reduce those risks.

### 2. Important Assets

| Asset | Why it needs protection |
|---|---|
| User accounts | Prevent account theft |
| Password hashes | Protect user credentials |
| User profiles | Protect personal information |
| Scan history | Maintain data privacy |
| Uploaded images | Prevent malicious file uploads |
| SQLite database | Prevent unauthorized access and modification |
| Flask secret key | Protect application sessions |

### 3. Potential Attackers

1. Malicious users attempting to access other users' accounts.
2. Attackers attempting SQL injection.
3. Users uploading malformed or oversized images.
4. Attackers attempting to steal login sessions.
5. Attackers attempting to submit malicious input through forms.

### 4. Identified Threats and Mitigations

| Threat | Possible impact | Security control |
|---|---|---|
| SQL Injection | Unauthorized database access | Parameterized SQL queries |
| Cross-Site Scripting (XSS) | Malicious scripts in browser | Input handling and output escaping |
| Cross-Site Request Forgery (CSRF) | Unauthorized actions | CSRF tokens |
| Weak Password Security | Account compromise | Salted PBKDF2 password hashing |
| Session Theft | Unauthorized account access | Secure session cookie settings |
| Unauthorized Record Access | Exposure of another user's scans | User ownership checks |
| Malicious File Upload | Application or server compromise | File validation and size limits |
| Denial of Service | Application slowdown or outage | Request and resource limits |
| Information Disclosure | Exposure of sensitive information | Safe error handling and production configuration |

### 5. Security Priorities

The following issues require particular attention:

- Replace the hardcoded Flask secret key.
- Disable Flask debug mode in production.
- Implement CSRF protection.
- Review all database queries.
- Strengthen file-upload and OCR protections.
- Add login rate limiting.
- Review session security settings.
- Test access controls for every user-specific record.

### 6. Threat Modeling Conclusion

Threat modeling helps identify risks before they become security problems. Karachi JobShield will use these identified threats to guide secure design, implementation, and testing.

**Note:** These are identified potential threats. Their actual exploitability must be verified through security testing.