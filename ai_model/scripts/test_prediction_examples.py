
from ai_model.predictor import load_ai_components


# Load the trained model and vectorizer
model, vectorizer = load_ai_components()


# Sample advertisements for testing
test_ads = [
    {
        "name": "Registration fee request",
        "text": "Pay a registration fee of $100 to secure your job."
    },
    {
        "name": "Bank details request",
        "text": "Send your bank password and ATM PIN to receive your salary."
    },
    {
        "name": "Normal job advertisement",
        "text": "We are hiring an accountant. Apply through our official company website."
    },
    {
        "name": "Unrealistic salary offer",
        "text": "Earn $5000 every week without experience or an interview."
    }
]


# Test each advertisement
for ad in test_ads:

    text_vector = vectorizer.transform([ad["text"]])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]

    print("\nAdvertisement:", ad["name"])

    print(
        "Prediction:",
        "Fraudulent" if prediction == 1 else "Genuine"
    )

    print("Genuine score:", round(probabilities[0] * 100, 2), "%")

    print("Fraudulent score:", round(probabilities[1] * 100, 2), "%")

