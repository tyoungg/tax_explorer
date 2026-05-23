import streamlit as st

st.set_page_config(page_title="Methodology", page_icon="📖")

st.title("📖 Methodology & Accuracy")

st.markdown("""
### Core Logic
This application uses the **Decimal** library in Python to perform all financial calculations.
Unlike standard floating-point numbers (which can suffer from binary approximation errors like `0.1 + 0.2 != 0.3`),
`Decimal` maintains exact precision for currency.

### Rounding Rules
1. **Sales Tax:** Rounded to the nearest cent (`$0.01`). If the tax is exactly between two cents, we round up (ROUND_HALF_UP).
2. **Total Calculation:** `Total = Shelf Price + Sales Tax`.
3. **Nickel Rounding:** Applied only to the final total.
   - `.01, .02` round down to `.00`
   - `.03, .04` round up to `.05`
   - `.06, .07` round down to `.05`
   - `.08, .09` round up to `.10`

### Data Sources
- **Florida Tax Rates:** Based on the Florida Department of Revenue's discretionary sales surtax rates by county.
- **Simulations:** Synthetic data is generated using NumPy, applying typical retail pricing patterns (e.g., preference for `.99` endings).

### Project Goals
This project aims to demonstrate how seemingly insignificant rounding rules can create systematic economic effects when applied at scale across millions of transactions.
""")

st.code("""
# The core rounding function used in this app
from decimal import Decimal, ROUND_HALF_UP

def nickel_round(amount: Decimal) -> Decimal:
    return (amount * Decimal('20')).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / Decimal('20')
""", language="python")
