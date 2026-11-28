import csv
import os
input_file = "ai_model/data/fake_job_postings.csv"
output_file = "ai_model/data/prepared_jobs.csv"

print("Preparing Karachi JobShield training dataset...")
text_columns = [
    "title",
    "location",
    "department",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

target_column = "fraudulent"
rows_written = 0

with open(input_file, "r", encoding="utf-8-sig", newline="") as source:
    reader = csv.DictReader(source)

    with open(output_file, "w", encoding="utf-8", newline="") as destination:
        fieldnames = ["text", target_column]
        writer = csv.DictWriter(destination, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            combined_text = " ".join(
                (row.get(column) or "").strip()
                for column in text_columns
            )

            label = (row.get(target_column) or "").strip()

            if label in {"0", "1"} and combined_text:
                writer.writerow({
                    "text": combined_text,
                    "fraudulent": label
                })
                rows_written += 1

print("Prepared advertisements:", rows_written)
print("Saved dataset:", output_file)
