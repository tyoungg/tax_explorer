import streamlit as st
from decimal import Decimal
from utils.rounding import transaction_effect

st.set_page_config(page_title="Single Transaction Explorer", page_icon="🪙")

st.title("Single Transaction Explorer")

st.markdown("Enter a price and tax rate to see exactly how the rounding math works.")

col1, col2 = st.columns(2)

with col1:
    price = st.number_input("Shelf Price ($)", min_value=0.01, value=9.99, step=0.01, format="%.2f")
    tax_rate_pct = st.number_input("Tax Rate (%)", min_value=0.0, max_value=20.0, value=7.50, step=0.25, format="%.2f")

tax_rate = Decimal(str(tax_rate_pct)) / 100
res = transaction_effect(Decimal(str(price)), tax_rate)

with col2:
    st.subheader("Calculation Breakdown")

    data = [
        ("Shelf Price", f"${res['price']:,.2f}"),
        ("Tax", f"${res['tax']:,.2f}"),
        ("Total (Pre-rounding)", f"${res['total']:,.2f}"),
        ("Rounded Total (Cash)", f"${res['rounded']:,.2f}"),
    ]

    for label, value in data:
        st.write(f"**{label}:** {value}")

    effect = res['effect']
    if effect > 0:
        st.error(f"**Effect:** +${effect:,.2f} (Retailer Gain)")
    elif effect < 0:
        st.success(f"**Effect:** -${abs(effect):,.2f} (Consumer Gain)")
    else:
        st.info("**Effect:** Neutral ($0.00)")

st.markdown("""
### How it works
1. **Tax Calculation:** The shelf price is multiplied by the tax rate and rounded to the nearest cent.
2. **Summing:** The shelf price and tax are added together.
3. **Nickel Rounding:** The total is rounded to the nearest $0.05.
4. **Rounding Effect:** The difference between the rounded total and the exact total.
""")
