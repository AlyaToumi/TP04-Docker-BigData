
from pathlib import Path
import pandas as pd

# TP04 - Sales Data Analysis
# Dataset previously used in TP03

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "train.csv"

print("=" * 55)
print("TP04 - BIG DATA ANALYTICS WITH DOCKER")
print("=" * 55)

# 1. Load dataset
df = pd.read_csv(DATA_FILE)

# 2. Dataset information
print("\n1. DATASET INFORMATION")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 3. Data quality
print("\n2. DATA QUALITY")
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

# 4. Total sales
print("\n3. TOTAL SALES")
print(f"Total sales: {df['Sales'].sum():,.2f}")

# 5. Sales by region
print("\n4. SALES BY REGION")
print(
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .to_string()
)

# 6. Sales by category
print("\n5. SALES BY CATEGORY")
print(
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .to_string()
)

# 7. Top 10 sub-categories
print("\n6. TOP 10 SUB-CATEGORIES")
print(
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_string()
)

print("\nAnalysis completed successfully!")


