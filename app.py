import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Customer Churn Dashboard", page_icon="📊", layout="wide")

# 2. Built-in Data Generator (No external CSV needed)
@st.cache_data
def load_data():
    """Generates 1,000 rows of realistic Telco customer data."""
    np.random.seed(42)
    n = 1000
    
    # Generate realistic correlations (e.g., month-to-month churns more)
    contracts = np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.25, 0.20])
    churn_probs = {"Month-to-month": 0.40, "One year": 0.11, "Two year": 0.03}
    churn = [np.random.choice(["Yes", "No"], p=[churn_probs[c], 1-churn_probs[c]]) for c in contracts]
    
    data = {
        "CustomerID": [f"CUST-{str(i).zfill(4)}" for i in range(1, n+1)],
        "Contract": contracts,
        "Tenure (Months)": np.random.randint(1, 72, n),
        "MonthlyCharges": np.random.uniform(20.0, 115.0, n),
        "TechSupport": np.random.choice(["Yes", "No", "No internet"], n, p=[0.29, 0.49, 0.22]),
        "Churn": churn
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Dashboard Header
st.title("📊 Customer Churn Analysis")
st.markdown("Analyzing customer retention trends and quantifying revenue at risk.")

# 4. Interactive Sidebar Filters
st.sidebar.header("Interactive Filters")
selected_contracts = st.sidebar.multiselect(
    "Filter by Contract Type:",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

# Apply filters
filtered_df = df[df["Contract"].isin(selected_contracts)]

# 5. Calculate Key Performance Indicators (KPIs)
total_customers = len(filtered_df)
churned_customers = len(filtered_df[filtered_df["Churn"] == "Yes"])
churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
revenue_at_risk = filtered_df[filtered_df["Churn"] == "Yes"]["MonthlyCharges"].sum()

# 6. Render KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Customers", value=f"{total_customers:,}")
col2.metric(label="Overall Churn Rate", value=f"{churn_rate:.1f}%")
col3.metric(label="Monthly Revenue at Risk", value=f"${revenue_at_risk:,.2f}")

st.markdown("---")

# 7. Render Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Churn by Contract Type")
    # Bar chart showing churn volume per contract
    fig_contract = px.histogram(
        filtered_df, 
        x="Contract", 
        color="Churn", 
        barmode="group",
        color_discrete_sequence=["#1f77b4", "#d62728"]
    )
    fig_contract.update_layout(xaxis_title="Contract Type", yaxis_title="Number of Customers")
    st.plotly_chart(fig_contract, use_container_width=True)

with col_right:
    st.subheader("Tenure Distribution (Stayed vs. Left)")
    # Box plot showing how long customers stay before churning
    fig_tenure = px.box(
        filtered_df, 
        x="Churn", 
        y="Tenure (Months)", 
        color="Churn",
        color_discrete_sequence=["#1f77b4", "#d62728"]
    )
    st.plotly_chart(fig_tenure, use_container_width=True)

st.subheader("Revenue vs. Tenure Analysis")
# Scatter plot mapping high-value customers
fig_scatter = px.scatter(
    filtered_df, 
    x="Tenure (Months)", 
    y="MonthlyCharges", 
    color="Churn", 
    opacity=0.7,
    color_discrete_sequence=["#1f77b4", "#d62728"]
)
fig_scatter.update_layout(xaxis_title="Customer Lifespan (Months)", yaxis_title="Monthly Bill ($)")
st.plotly_chart(fig_scatter, use_container_width=True)