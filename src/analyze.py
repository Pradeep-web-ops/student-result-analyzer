# src/analyze.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "students_marks.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)

# Basic cleaning: ensure marks numeric, fill missing with 0 or median
subject_cols = [c for c in df.columns if c not in ("StudentID", "Name")]
for c in subject_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')
    df[c] = df[c].fillna(df[c].median())

# Compute total, average, grade
df["Total"] = df[subject_cols].sum(axis=1)
df["Average"] = df[subject_cols].mean(axis=1)

def grade(avg):
    if avg >= 90: return "A+"
    if avg >= 80: return "A"
    if avg >= 70: return "B+"
    if avg >= 60: return "B"
    if avg >= 50: return "C"
    return "D"

df["Grade"] = df["Average"].apply(grade)

# Save summary CSV
os.makedirs(OUTPUT_DIR, exist_ok=True)
summary_csv = os.path.join(OUTPUT_DIR, "summary.csv")
df.to_csv(summary_csv, index=False)

# Top performers
top_n = 5
top_df = df.sort_values(by="Total", ascending=False).head(top_n)

# Plot: Top performers bar chart
plt.figure(figsize=(8,5))
plt.bar(top_df["Name"], top_df["Total"])
plt.title(f"Top {top_n} Performers by Total Marks")
plt.xlabel("Student")
plt.ylabel("Total Marks")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "top_performers.png"))
plt.close()

# Plot: Subject-wise average distribution
subject_means = df[subject_cols].mean()
plt.figure(figsize=(8,5))
subject_means.plot(kind="bar")
plt.title("Average Marks per Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "subject_average.png"))
plt.close()

# Plot: Grade distribution pie chart
grade_counts = df["Grade"].value_counts()
plt.figure(figsize=(6,6))
grade_counts.plot(kind="pie", autopct="%1.1f%%")
plt.title("Grade Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "grade_distribution.png"))
plt.close()

print("Analysis completed.")
print(f"Summary saved to: {summary_csv}")
print(f"Plots saved to: {PLOTS_DIR}")
