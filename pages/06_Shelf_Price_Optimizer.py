import streamlit as st
import pandas as pd
import numpy as np
from utils.simulation import run_simulation

st.set_page_config(page_title="Shelf Price Optimizer", page_icon="🎯", layout="wide")

st.title("🎯 Shelf Price Optimizer")

st.markdown("""
Which specific prices are most 'optimal' for the retailer or the consumer?
This page searches a price range to find values that consistently round up or down.
""")

col1, col2 = st.columns([1, 2])

with col1:
    tax_rate_pct = st.number_input("Tax Rate (%)", 0.0, 15.0, 7.5, 0.1)
    min_p = st.number_input("Min Price ($)", 0.01, 100.0, 1.0)
    max_p = st.number_input("Max Price ($)", 1.0, 500.0, 50.0)

    st.write("---")
    uploaded_file = st.file_uploader("Optional: Upload SKU/Price CSV", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    if 'PRICE' in input_df.columns:
        prices = input_df['PRICE'].tolist()
        st.success(f"Loaded {len(prices)} prices from file.")
    else:
        st.error("CSV must have a 'PRICE' column.")
        prices = np.arange(min_p, max_p, 0.01)
else:
    # Default to sweeping the range
    prices = np.arange(min_p, max_p, 0.01)

if st.button("Analyze Prices"):
    with st.spinner("Analyzing..."):
        df = run_simulation(prices, tax_rate_pct / 100)

        with col2:
            best_retailer = df.sort_values('effect', ascending=False).head(10)
            best_consumer = df.sort_values('effect', ascending=True).head(10)

            st.subheader("Top 10 'Retailer-Friendly' Prices (+2¢)")
            st.table(best_retailer[['price', 'total', 'rounded', 'effect']].style.format({'price': '{:.2f}', 'total': '{:.2f}', 'rounded': '{:.2f}', 'effect': '{:+.2f}'}))

            st.subheader("Top 10 'Consumer-Friendly' Prices (-2¢)")
            st.table(best_consumer[['price', 'total', 'rounded', 'effect']].style.format({'price': '{:.2f}', 'total': '{:.2f}', 'rounded': '{:.2f}', 'effect': '{:+.2f}'}))

st.markdown("""
### Strategy
- **Retailers:** To maximize rounding gains, aim for prices where `(Price * (1 + Tax))` ends in `.03, .04, .08, or .09`.
- **Consumers:** To maximize savings, look for prices where the post-tax total ends in `.01, .02, .06, or .07`.
""")
