import pandas as pd
import numpy as np
import os

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

FILE_PATH = "data/expenses.csv"


# ----------------------------------------
# 1. CREATE SYNTHETIC DATA (INITIAL SETUP)
# ----------------------------------------
def generate_data(n=300):
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", periods=180)

    categories = ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment"]
    payment_methods = ["Cash", "Card", "UPI"]

    df = pd.DataFrame({
        "date": np.random.choice(dates, n),
        "category": np.random.choice(categories, n),
        "amount": np.random.randint(100, 5000, n),
        "payment_method": np.random.choice(payment_methods, n)
    })

    df.to_csv(FILE_PATH, index=False)
    return df


# ----------------------------------------
# 2. LOAD DATA
# ----------------------------------------
def load_data():
    if not os.path.exists(FILE_PATH):
        return generate_data()

    df = pd.read_csv(FILE_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df


# ----------------------------------------
# 3. ADD NEW EXPENSE (USER INPUT)
# ----------------------------------------
def add_expense(date, category, amount, payment_method):
    df = load_data()

    new_entry = pd.DataFrame({
        "date": [pd.to_datetime(date)],
        "category": [category],
        "amount": [amount],
        "payment_method": [payment_method]
    })

    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    return df


# ----------------------------------------
# 4. CLEAN + FEATURE ENGINEERING
# ----------------------------------------
def process_data(df):
    df = df.dropna()

    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df


# ----------------------------------------
# 5. ANALYSIS FUNCTIONS
# ----------------------------------------
def category_summary(df):
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)


def monthly_summary(df):
    return df.groupby("month")["amount"].sum()


def payment_summary(df):
    return df.groupby("payment_method")["amount"].sum()


# ----------------------------------------
# 6. INSIGHTS
# ----------------------------------------
def generate_insights(df):
    cat = category_summary(df)
    mon = monthly_summary(df)

    insights = {
        "top_category": cat.idxmax(),
        "top_category_value": cat.max(),
        "top_month": mon.idxmax(),
        "top_month_value": mon.max()
    }

    return insights