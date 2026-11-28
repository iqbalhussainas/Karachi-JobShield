
from huggingface_hub import HfApi

# Connect to Hugging Face
api = HfApi()

# Your private repository
repo_id = "techiq12/karachi-jobshield-ai"

print("Uploading Karachi JobShield AI model...")

# Upload trained model
api.upload_file(
    path_or_fileobj="ai_model/models/jobshield_model.pkl",
    path_in_repo="jobshield_model.pkl",
    repo_id=repo_id,
    repo_type="model"
)

print("AI model uploaded successfully!")

# Upload TF-IDF vectorizer
api.upload_file(
    path_or_fileobj="ai_model/models/tfidf_vectorizer.pkl",
    path_in_repo="tfidf_vectorizer.pkl",
    repo_id=repo_id,
    repo_type="model"
)

print("TF-IDF vectorizer uploaded successfully!")
print("Karachi JobShield upload completed!")
