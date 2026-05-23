import streamlit as st
import pandas as pd
import numpy as np
from utils.simulation import run_simulation
from utils.charts import plot_heatmap

st.set_page_config(page_title="Rounding Heatmaps", page_icon="🌡️", layout="wide")

st.title("🌡️ Rounding Impact Heatmaps")

st.markdown("""
This visualization shows how rounding bias changes as both **Tax Rate** and **Price Ending** vary.
It helps identify "hot zones" where retailers consistently gain and "cool zones" where consumers benefit.
""")

col1, col2 = st.columns([1, 4])

with col1:
    min_tax = st.slider("Min Tax Rate (%)", 0.0, 10.0, 6.0, 0.5)
    max_tax = st.slider("Max Tax Rate (%)", 5.0, 15.0, 9.0, 0.5)
    tax_step = st.selectbox("Tax Step (%)", [0.1, 0.25, 0.5], index=1)

    price_endings = [".00", ".49", ".79", ".88", ".95", ".99"]

tax_rates = np.arange(min_tax, max_tax + tax_step, tax_step)

heatmap_data = []

# To make it representative, we sample $1 to $50 for each combination
sample_prices_base = list(range(1, 51))

with st.spinner("Calculating Heatmap..."):
    for tr in tax_rates:
        for ending in price_endings:
            prices = [float(p) + float(ending) for p in sample_prices_base]
            df = run_simulation(prices, tr / 100)
            avg_bias = df['effect'].mean()
            heatmap_data.append({
                'Tax Rate (%)': tr,
                'Price Ending': ending,
                'Avg Bias': avg_bias
            })

h_df = pd.DataFrame(heatmap_data)

with col2:
    fig = plot_heatmap(
        h_df,
        x_col='Price Ending',
        y_col='Tax Rate (%)',
        z_col='Avg Bias',
        title="Avg Bias by Tax Rate and Price Ending"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### How to read this
- **Dark Red:** Strong Retailer Advantage (+1¢ or more on average)
- **Dark Blue:** Strong Consumer Advantage (-1¢ or more on average)
- **White/Pale:** Nearly Neutral
""")
