# Nickel Rounding Simulator

A multi-tab Streamlit application to explore the economic impact of cash transaction rounding.

## Overview
In many jurisdictions, the discontinuation of the penny leads to rounding of cash transactions to the nearest $0.05. This app simulates and visualizes how this rounding affects consumers and retailers differently depending on tax rates, price endings, and transaction volume.

## Features
- **Single Transaction Explorer:** Understand the step-by-step math.
- **Price Ending Explorer:** Analyze how prices ending in `.99`, `.95`, etc., interact with taxes.
- **Tax Rate Explorer:** Sweep through tax rates to find "resonance" points of high bias.
- **Florida County Comparison:** Compare expected bias across all Florida counties.
- **Monte Carlo Simulator:** Run millions of transactions to see long-term annualized impacts.
- **Shelf Price Optimizer:** Find the most "fair" or "profitable" prices.
- **Rounding Heatmaps:** Visualize the interaction between price endings and tax rates.

## Architecture
- `app.py`: Main entry point and landing page.
- `pages/`: Individual analysis tools.
- `utils/`: Core logic for rounding, simulation, and charts.
- `data/`: Florida tax rate datasets.

## Technical Stack
- **Streamlit:** Frontend and interactivity.
- **Pandas/NumPy:** Data processing and simulation.
- **Plotly:** Dynamic visualizations.
- **Decimal:** High-precision financial arithmetic.

## Getting Started
```bash
pip install streamlit pandas numpy plotly scipy matplotlib
streamlit run app.py
```
