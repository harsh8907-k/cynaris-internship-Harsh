
import pandas as pd
import numpy as np
from pathlib import Path

# Project folder
BASE_DIR = Path(__file__).resolve().parent
original_file = BASE_DIR / "original_dataset.csv"

# 1. Create original dataset only if it does not exist
if not original_file.exists():
    source_data = {
        "name": [" Alice ", "BOB", "alice", "David ", None, "Eva"],
        "age": [25, 30, np.nan, 200, 40, 28],
        "salary": [30000, 45000, 35000, 50000, np.nan, 1000000],
        "city": [
            "Bangalore", "mumbai", "BANGALORE ",
            "Delhi", "Pune", None
        ],
        "department": ["IT", "HR", "IT", "Finance", "HR", "IT"]
    }
    pd.DataFrame(source_data).to_csv(original_file, index=False)

# 2. Load the original data
original_df = pd.read_csv(original_file)
df = original_df.copy()

# 3. Record data quality before cleaning
rows_before = len(df)
missing_before = int(df.isnull().sum().sum())
duplicates_before = int(df.duplicated().sum())

missing_details = df.isnull().sum()

# 4. Normalize text and whitespace
for col in ["name", "city", "department"]:
    df[col] = df[col].astype("string").str.strip()

# Consistent capitalization
df["name"] = df["name"].str.title()
df["city"] = df["city"].str.title()
df["department"] = df["department"].str.upper()

# Convert empty strings to missing values
for col in ["name", "city", "department"]:
    df[col] = df[col].replace("", pd.NA)

# 5. Impute missing values
age_mean = df["age"].mean()
age_median = df["age"].median()
salary_median = df["salary"].median()
city_mode = df["city"].mode().iloc[0]

# Demonstrate mean imputation
df["age"] = df["age"].fillna(age_mean)

# Demonstrate median imputation
df["salary"] = df["salary"].fillna(salary_median)

# Demonstrate mode imputation
df["city"] = df["city"].fillna(city_mode)

# Fill missing names
df["name"] = df["name"].fillna("Unknown")

# Demonstrate forward-fill separately without changing original data
forward_fill_example = original_df["department"].ffill()
forward_fill_missing_after = int(forward_fill_example.isna().sum())

# 6. Correct invalid ages
invalid_age_count = int(
    ((df["age"] < 0) | (df["age"] > 100)).sum()
)

df.loc[(df["age"] < 0) | (df["age"] > 100), "age"] = np.nan
df["age"] = df["age"].fillna(df["age"].median())

# 7. Detect and cap outliers using the IQR method
outlier_log = []

for col in ["age", "salary"]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_count = int(
        ((df[col] < lower) | (df[col] > upper)).sum()
    )

    outlier_log.append(
        f"- {col}: {outlier_count} outliers detected; "
        f"capped to [{lower:.2f}, {upper:.2f}]"
    )

    df[col] = df[col].clip(lower=lower, upper=upper)

# 8. Remove duplicate rows
df = df.drop_duplicates()

# 9. Save cleaned dataset
df.to_csv(BASE_DIR / "cleaned_dataset.csv", index=False)

# 10. Create before-and-after quality comparison
comparison = pd.DataFrame({
    "Metric": ["Rows", "Missing values", "Duplicate rows"],
    "Before": [
        rows_before,
        missing_before,
        duplicates_before
    ],
    "After": [
        len(df),
        int(df.isnull().sum().sum()),
        int(df.duplicated().sum())
    ]
})

comparison.to_csv(
    BASE_DIR / "data_quality_comparison.csv",
    index=False
)

# 11. Create cleaning log
log = [
    "# Data Cleaning Log",
    "",
    "## Dataset",
    "Sample employee dataset used for Week 2 Day 4 practice.",
    "",
    "## Missing values before cleaning",
    missing_details.to_string(),
    "",
    "## Cleaning decisions",
    "- Trimmed whitespace from text columns.",
    "- Standardized names and cities using title case.",
    "- Standardized department values to uppercase.",
    "- Imputed missing age using the mean.",
    "- Imputed missing salary using the median.",
    "- Imputed missing city using the mode.",
    "- Replaced missing names with 'Unknown'.",
    "- Demonstrated forward-fill on a separate department Series.",
    "- Corrected ages outside the 0-100 range using the median.",
    "- Detected numeric outliers using the 1.5 x IQR rule.",
    "- Capped detected numeric outliers at the IQR boundaries.",
    "- Removed duplicate rows where present.",
    "",
    "## Imputation reference values",
    f"- Original age mean: {age_mean:.2f}",
    f"- Original age median: {age_median:.2f}",
    f"- Original salary median: {salary_median:.2f}",
    f"- City mode: {city_mode}",
    f"- Missing departments after forward-fill: "
    f"{forward_fill_missing_after}",
    "",
    "## Invalid ages",
    f"- Invalid ages corrected: {invalid_age_count}",
    "",
    "## Outlier detection",
    *outlier_log,
    "",
    "## Before-and-after quality comparison",
    comparison.to_string(index=False),
    "",
    "## Final missing values",
    df.isnull().sum().to_string()
]

(BASE_DIR / "cleaning_log.md").write_text(
    "\n".join(log),
    encoding="utf-8"
)

# 12. Display results
print("Data cleaning completed successfully!")
print("\nBefore-and-after comparison:")
print(comparison)

print("\nCleaned dataset:")
print(df)

print("\nFiles saved:")
print("cleaned_dataset.csv")
print("cleaning_log.md")
print("data_quality_comparison.csv")
