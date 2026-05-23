import streamlit as st

st.set_page_config(
    page_title="Nickel Rounding Simulator",
    page_icon="🪙",
    layout="wide"
)

st.title("🪙 The Hidden Math of Nickel Rounding")

st.markdown("""
Welcome to the **Nickel Rounding Simulator**.

In jurisdictions where pennies are no longer used for cash transactions (or where custom rounding rules apply),
the final total is often rounded to the nearest 5 cents. While a single transaction might only be rounded
by ±1 or 2 cents, these effects can accumulate over thousands of transactions, creating a systematic
bias that favors either the consumer or the retailer.

### Explore the Impact:
- **Single Transaction:** Get intuition for how one purchase is affected.
- **Price Endings:** See how common endings like `.99` interact with taxes.
- **Tax Rate Explorer:** Find 'resonance' effects where certain tax rates cause high bias.
- **County Comparison:** Compare the expected bias across Florida's 67 counties.
- **Monte Carlo Simulator:** Run millions of synthetic transactions to see long-term impact.
- **Shelf Price Optimizer:** Find the most "fair" (or profitable) prices for your inventory.
- **Heatmaps:** Visualize the interaction between price endings and tax rates.

Use the sidebar to navigate between different analysis tools.
""")

st.sidebar.success("Select a page above.")

st.info("💡 **Tip:** This app uses `Decimal` arithmetic for financial accuracy, avoiding the floating-point errors common in simple calculators.")
