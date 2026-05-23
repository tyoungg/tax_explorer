import streamlit as st
import pandas as pd
from decimal import Decimal
from utils.simulation import run_simulation
from utils.charts import plot_bias_line_chart

st.set_page_config(page_title="Tax Rate Explorer", page_icon="📈", layout="wide")

st.title("📈 Tax Rate Explorer")

st.markdown("""
Do certain tax rates produce more rounding bias than others?
By fixing a price ending and sweeping through various tax rates, we can find 'resonance' points.
""")

col1, col2 = st.columns([1, 3])

with col1:
    price_ending = st.number_input("Price Ending (e.g., 0.99)", 0.00, 0.99, 0.99, 0.01)
    min_tax = st.slider("Min Tax Rate (%)", 0.0, 10.0, 5.0, 0.1)
    max_tax = st.slider("Max Tax Rate (%)", 5.0, 15.0, 10.0, 0.1)
    step = st.number_input("Step size (%)", 0.01, 1.0, 0.1)

tax_rates = []
curr = min_tax
while curr <= max_tax:
    tax_rates.append(curr)
    curr += step

# Use a more diverse set of sample prices to avoid integer cancellation effects
# Mixing small, medium, and large prices
sample_prices = []
for base in [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 250.0, 500.0]:
    sample_prices.append(base + price_ending)
    sample_prices.append(base * 1.5 + price_ending)

bias_results = []
for tr in tax_rates:
    df = run_simulation(sample_prices, tr / 100)
    avg_bias = df['effect'].mean()
    bias_results.append({'tax_rate': tr, 'avg_bias': avg_bias})

bias_df = pd.DataFrame(bias_results)

with col2:
    fig = plot_bias_line_chart(
        bias_df,
        'tax_rate',
        'avg_bias',
        title=f"Average Bias vs Tax Rate (Prices ending in .{int(price_ending*100):02d})",
        x_label="Tax Rate (%)",
        y_label="Average Bias ($)"
    )
    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    ### Observations
    - **Upward Bias:** Points above the red dashed line favor the retailer.
    - **Downward Bias:** Points below the red dashed line favor the consumer.
    - **Resonance:** Notice how the bias oscillates. Small changes in tax rates (like a 0.5% increase) can significantly shift the rounding advantage.
    """)
