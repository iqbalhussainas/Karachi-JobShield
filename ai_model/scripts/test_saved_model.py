
import joblib

# Load the saved AI model
model = joblib.load("ai_model/models/jobshield_model.pkl")

# Load the saved TF-IDF vectorizer
vectorizer = joblib.load("ai_model/models/tfidf_vectorizer.pkl")

print("Saved AI model loaded successfully!")

# Example job advertisement
job_text = """
We are hiring a Data Entry Operator.
No experience required.
Earn $5000 per week.
Pay a registration fee of $100 to secure your job.
Send your bank details immediately.
"""

# Convert advertisement into numerical features
job_vector = vectorizer.transform([job_text])

# Predict advertisement
prediction = model.predict(job_vector)[0]

# Display result
print("\nJob Advertisement Analysis:")

if prediction == 1:
    print("Warning: This advertisement appears FRAUDULENT!")
else:
    print("This advertisement appears GENUINE.")
