
import joblib

# Load model downloaded from Hugging Face
model = joblib.load(
    "ai_model/hf_downloaded/jobshield_model.pkl"
)

# Load downloaded TF-IDF vectorizer
vectorizer = joblib.load(
    "ai_model/hf_downloaded/tfidf_vectorizer.pkl"
)

print("Hugging Face model loaded successfully!")

# Test job advertisement
job_text = """
We are hiring a Data Entry Operator.
No experience required.
Earn $5000 per week.
Pay a registration fee of $100 to secure your job.
Send your bank details immediately.
"""

# Convert text into numerical features
job_vector = vectorizer.transform([job_text])

# Predict advertisement
prediction = model.predict(job_vector)[0]

print("\nHugging Face Model Prediction:")

if prediction == 1:
    print("Warning: This advertisement appears FRAUDULENT!")
else:
    print("This advertisement appears GENUINE.")
