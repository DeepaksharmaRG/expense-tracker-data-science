import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from main import (
    load_data,
    add_expense,
    process_data,
    category_summary,
    monthly_summary,
    payment_summary,
    generate_insights
)

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker App (Data Science Project)")

# ----------------------------------------
# LOAD DATA
# ----------------------------------------
df = load_data()
df = process_data(df)

# ----------------------------------------
# SIDEBAR INPUT
# ----------------------------------------
st.sidebar.header("➕ Add New Expense")

date = st.sidebar.date_input("Date")
category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment"]
)
amount = st.sidebar.number_input("Amount", min_value=0)
payment = st.sidebar.selectbox("Payment Method", ["Cash", "Card", "UPI"])

if st.sidebar.button("Add Expense"):
    df = add_expense(date, category, amount, payment)
    df = process_data(df)
    st.sidebar.success("Expense Added Successfully!")

# ----------------------------------------
# DATA PREVIEW
# ----------------------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.tail(10))

# ----------------------------------------
# KPIs
# ----------------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Spending", f"₹ {df['amount'].sum():,.0f}")
col2.metric("Total Transactions", len(df))
col3.metric("Average Spending", f"₹ {df['amount'].mean():,.0f}")

# ----------------------------------------
# CATEGORY ANALYSIS
# ----------------------------------------
st.subheader("📌 Category-wise Spending")

cat_data = category_summary(df)

fig1, ax1 = plt.subplots()
cat_data.plot(kind="bar", ax=ax1)
plt.xticks(rotation=45)

st.pyplot(fig1)

# ----------------------------------------
# MONTHLY TREND
# ----------------------------------------
st.subheader("📈 Monthly Spending Trend")

mon_data = monthly_summary(df)

fig2, ax2 = plt.subplots()
mon_data.plot(marker='o', ax=ax2)

st.pyplot(fig2)

# ----------------------------------------
# PAYMENT METHOD
# ----------------------------------------
st.subheader("💳 Payment Method Analysis")

pay_data = payment_summary(df)

fig3, ax3 = plt.subplots()
pay_data.plot(kind="pie", autopct='%1.1f%%', ax=ax3)

st.pyplot(fig3)

# ----------------------------------------
# INSIGHTS
# ----------------------------------------
st.subheader("🔍 Insights")

insights = generate_insights(df)

st.write(f"💡 Highest Spending Category: **{insights['top_category']}** (₹ {insights['top_category_value']})")
st.write(f"📅 Highest Spending Month: **{insights['top_month']}** (₹ {insights['top_month_value']})")