import streamlit as st
import pandas as pd
from utils.tax_rates import load_florida_tax_rates
from utils.simulation import run_simulation

st.set_page_config(page_title="Florida County Comparison", page_icon="🗺️", layout="wide")

st.title("🗺️ Florida County Comparison")

st.markdown("""
Which Florida counties are most 'friendly' to consumers vs retailers?
This analysis assumes a set of prices (e.g., all ending in `.99`) and calculates the expected
rounding bias based on each county's specific tax rate.
""")

col1, col2 = st.columns([1, 2])

with col1:
    price_ending = st.selectbox("Shelf Price Ending", [0.99, 0.95, 0.49, 0.00, "Random"])
    n_samples = st.slider("Number of Sample Prices", 10, 500, 100)

if price_ending == "Random":
    import numpy as np
    sample_prices = np.random.uniform(1.0, 100.0, n_samples)
else:
    # Mix integers and semi-integers to avoid systematic cancellation
    sample_prices = []
    for i in range(1, n_samples + 1):
        sample_prices.append(float(i) + price_ending)
        if len(sample_prices) >= n_samples: break
        sample_prices.append(float(i) * 1.45 + price_ending)
        if len(sample_prices) >= n_samples: break

tax_df = load_florida_tax_rates()

results = []
for index, row in tax_df.iterrows():
    county = row['County']
    rate = row['TaxRate']

    sim_df = run_simulation(sample_prices, rate)
    avg_bias = sim_df['effect'].mean()

    results.append({
        'County': county,
        'Tax Rate': f"{float(rate)*100:.2f}%",
        'Avg Bias ($)': avg_bias,
        'Bias Type': 'Retailer Gain' if avg_bias > 0 else 'Consumer Gain' if avg_bias < 0 else 'Neutral'
    })

res_df = pd.DataFrame(results).sort_values('Avg Bias ($)', ascending=False)

with col2:
    st.subheader("County Rankings")
    st.dataframe(res_df.style.background_gradient(subset=['Avg Bias ($)'], cmap='RdBu_r'), height=600, use_container_width=True)

st.markdown("""
### Interpretation
- **Red/Positive:** Counties where the rounding math slightly favors the retailer on average.
- **Blue/Negative:** Counties where the rounding math slightly favors the consumer.
- **Why?** Even small differences in local tax rates (6.5% vs 7.0% vs 7.5%) change the distribution of the final digit, shifting the rounding probability.
""")
