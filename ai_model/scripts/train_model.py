
import pandas as pd
import joblib

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# STEP 1: Load prepared dataset
data = pd.read_csv("ai_model/data/prepared_jobs.csv")

print("Dataset loaded successfully!")
print("Total records:", len(data))
print(data.head())


# STEP 2: Separate input text and target labels
X = data["text"]
y = data["fraudulent"]

print("Text data separated:", len(X))
print("Labels separated:", len(y))


# STEP 3: Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# STEP 4: Convert text into numerical features
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000
)

X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

print("Text converted into numerical features!")
print("Training feature shape:", X_train_vectors.shape)
print("Testing feature shape:", X_test_vectors.shape)


# STEP 5: Create Logistic Regression model
model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)


# STEP 6: Train the model
print("Training Karachi JobShield AI model...")

model.fit(X_train_vectors, y_train)

print("Model training completed!")


# STEP 7: Evaluate the trained model
y_pred = model.predict(X_test_vectors)

print("\nModel Evaluation Results:")

print(classification_report(
    y_test,
    y_pred,
    target_names=["Genuine", "Fraudulent"],
    zero_division=0
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# STEP 8: Save trained model and vectorizer

model_path = "ai_model/models/jobshield_model.pkl"
vectorizer_path = "ai_model/models/tfidf_vectorizer.pkl"

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("\nAI model saved successfully!")
print("Model:", model_path)
print("Vectorizer:", vectorizer_path)