import streamlit as st
import pandas as pd

st.title("Loan Amortization Schedule Calculator")

# Input widgets for loan details
loan_amount = st.number_input(
    label="Enter the loan amount:",
    min_value=1.0,
    value=100000.0,
    step=1000.0,
    format="%.2f"
)

annual_interest_rate = st.number_input(
    label="Enter the annual interest rate (in percentage):",
    min_value=0.01,
    value=5.0,
    step=0.1,
    format="%.2f"
)

loan_period_months = st.number_input(
    label="Enter the loan tenure in months:",
    min_value=1,
    value=60,
    step=1
)

# Calculate monthly interest rate and EMI
if annual_interest_rate > 0 and loan_period_months > 0:
    monthly_interest_rate = annual_interest_rate / 100 / 12
    emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** loan_period_months) / ((1 + monthly_interest_rate) ** loan_period_months - 1)
    
    # Round EMI to the nearest whole rupee
    emi_rounded = round(emi)
    
    st.header("Loan Details")
    st.write(f"**Monthly EMI:** ₹{emi_rounded:,.0f}")

    # Generate the amortization schedule
    amortization_schedule = []
    remaining_balance = loan_amount

    for month in range(1, loan_period_months + 1):
        interest_component = remaining_balance * monthly_interest_rate
        principal_component = emi_rounded - interest_component
        remaining_balance -= principal_component
        
        # Ensure remaining balance doesn't go below zero due to rounding
        if remaining_balance < 0:
            principal_component += remaining_balance
            remaining_balance = 0
        
        amortization_schedule.append({
            'Month': month,
            'EMI': f"₹{emi_rounded:,.0f}",
            'Principal': f"₹{principal_component:,.2f}",
            'Interest': f"₹{interest_component:,.2f}",
            'Remaining Balance': f"₹{remaining_balance:,.2f}"
        })