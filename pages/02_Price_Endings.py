import streamlit as st
import numpy as np
from utils.simulation import run_simulation
from utils.charts import plot_rounding_histogram, plot_last_digit_distribution

st.set_page_config(page_title="Price Ending Explorer", page_icon="🏷️", layout="wide")

st.title("🏷️ Price Ending Explorer")

st.markdown("""
Retailers often use specific endings like `.99` or `.95`.
This page explores how these endings interact with a specific tax rate across a range of dollar amounts.
""")

col1, col2 = st.columns([1, 3])

with col1:
    tax_rate_pct = st.slider("Tax Rate (%)", 0.0, 15.0, 7.0, 0.25)
    ending_type = st.selectbox("Price Ending", [".99", ".95", ".49", ".79", ".88", "Custom"])

    if ending_type == "Custom":
        ending_val = st.number_input("Custom Ending", 0.00, 0.99, 0.00, 0.01)
    else:
        ending_val = float(ending_type)

    max_price = st.number_input("Max Price ($)", 10, 1000, 100)

prices = [i + ending_val for i in range(0, max_price) if i + ending_val > 0]
df = run_simulation(prices, tax_rate_pct / 100)

with col2:
    avg_bias = df['effect'].mean()
    st.metric("Average Rounding Bias", f"{avg_bias:+.4f}$", delta_color="inverse")

    tab1, tab2 = st.tabs(["Histogram", "Last Digit Analysis"])

    with tab1:
        fig_hist = plot_rounding_histogram(df, title=f"Rounding Impact Distribution for {ending_type} prices")
        st.plotly_chart(fig_hist, use_container_width=True)

    with tab2:
        st.markdown("""
        **Post-Tax Last Digit Frequency**

        This chart shows how often each digit (0-9) appears in the *cents* place of the total **after tax** but **before rounding**.

        - **0, 5:** No rounding
        - **1, 2, 6, 7:** Rounding down
        - **3, 4, 8, 9:** Rounding up
        """)
        fig_digit = plot_last_digit_distribution(df)
        st.plotly_chart(fig_digit, use_container_width=True)

st.dataframe(df.style.format({
    'price': '{:.2f}',
    'tax': '{:.2f}',
    'total': '{:.2f}',
    'rounded': '{:.2f}',
    'effect': '{:+.2f}'
}), use_container_width=True)
