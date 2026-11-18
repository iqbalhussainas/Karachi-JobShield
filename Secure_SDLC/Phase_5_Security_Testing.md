# Karachi JobShield
# Phase 5 – Security Testing

**Project:** Karachi JobShield – Cybersecurity Awareness Center  
**Testing Date:** 15 November 2026  
**Environment:** Windows, Python, Flask, SQLite

## 1. Objective

The purpose of this phase is to test the security controls implemented in Karachi JobShield, particularly image upload validation and OCR processing.

## 2. Image Upload Security Test Results

| Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|
| Valid JPG image | Process image using OCR | Image processed successfully | PASS |
| TXT file upload | Reject unsupported file | Correct rejection message displayed | PASS |
| Unsupported image format | Reject unsupported format | File rejected with error message | PASS |
| Image without readable text | Reject empty OCR result | Correct error message displayed | PASS |
| Image exceeding 5 MB | Reject oversized upload | 16.99 MB image rejected | PASS |

## 3. Security Controls Verified

1. Server-side file extension validation.
2. Actual image format verification using Pillow.
3. Image dimension restrictions.
4. Maximum upload size of 5 MB.
5. OCR text extraction using Tesseract.
6. Handling of invalid and unreadable images.
7. User-friendly flash messages for errors.

## 4. Testing Evidence

The following results were observed during manual testing:

- Unsupported TXT file: "Only PNG, JPG and JPEG images are allowed."
- Unsupported image format: "The uploaded file is not a supported image."
- Empty OCR result: "No readable text was found. Please try a clearer job poster."
- Oversized upload: "Image is too large. Maximum upload size is 5 MB."

A valid JPG image was also successfully processed by the OCR feature.

## 5. Conclusion

The image upload security tests were completed successfully. The application correctly handled supported images, rejected unsupported files, detected images without readable text, and enforced the configured 5 MB upload limit.

These tests provide evidence that important image upload security controls are functioning as expected.

**Testing scope:** This report covers the listed manual tests only. It does not represent a complete penetration test or security audit.