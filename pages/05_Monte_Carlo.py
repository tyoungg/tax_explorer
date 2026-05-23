import streamlit as st
from utils.simulation import run_monte_carlo
from utils.charts import plot_rounding_histogram

st.set_page_config(page_title="Monte Carlo Simulator", page_icon="🎲", layout="wide")

st.title("🎲 Monte Carlo Simulator")

st.markdown("""
Simulate thousands of transactions to see how rounding effects accumulate in a "real-world" scenario.
""")

col1, col2 = st.columns([1, 2])

with col1:
    n_transactions = st.number_input("Number of Transactions", 1000, 1000000, 10000, 1000)
    tax_rate_pct = st.number_input("Tax Rate (%)", 0.0, 15.0, 7.5, 0.1)
    dist_type = st.selectbox("Price Distribution", ["realistic", "uniform"])

    cash_pct = st.slider("Percentage of Cash Transactions (%)", 0, 100, 30)

    run_btn = st.button("Run Simulation", type="primary")

if run_btn:
    with st.spinner("Simulating..."):
        df = run_monte_carlo(n_transactions, tax_rate_pct / 100, distribution=dist_type)

        # Only cash transactions are rounded
        cash_mask = df.index < (n_transactions * cash_pct / 100)
        total_effect = df.loc[cash_mask, 'effect'].sum()
        avg_effect = df.loc[cash_mask, 'effect'].mean()

        st.success(f"Simulated {n_transactions:,} transactions!")

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Rounding Impact", f"${total_effect:,.2f}")
        m2.metric("Average Bias/Cash Tx", f"${avg_effect:,.4f}")
        m3.metric("Annualized (1M Tx)", f"${(avg_effect * 1000000):,.2f}")

        with col2:
            fig = plot_rounding_histogram(df.loc[cash_mask], title="Distribution of Rounding Effects (Cash Only)")
            st.plotly_chart(fig, width='stretch')

            st.info(f"**Scenario:** In a business with {n_transactions:,} transactions where {cash_pct}% are cash, "
                    f"the {'retailer' if total_effect > 0 else 'consumer'} {'gained' if total_effect > 0 else 'saved'} "
                    f"a total of **${abs(total_effect):,.2f}** due to nickel rounding.")
else:
    st.info("Click 'Run Simulation' to start.")
