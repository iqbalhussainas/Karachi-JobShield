import csv
from collections import Counter
# Dataset location
file_path = "ai_model/data/fake_job_postings.csv"

print("Reading Karachi JobShield dataset...")

label_counts = Counter()
total_rows = 0
with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    print("\nDataset Columns:")
    print(reader.fieldnames)

    for row in reader:
        total_rows += 1
        label = row.get("fraudulent", "").strip()
        label_counts[label] += 1
        print("\nDataset Summary")
print("-----------------------")
print("Total advertisements:", total_rows)
print("Genuine jobs (0):", label_counts["0"])
print("Fraudulent jobs (1):", label_counts["1"])

print("\nDataset inspection completed!")