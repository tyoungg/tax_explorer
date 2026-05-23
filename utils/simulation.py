import pandas as pd
import numpy as np
from decimal import Decimal
from .rounding import transaction_effect

def run_simulation(prices, tax_rate):
    """
    Runs transaction effect calculations for a list of prices.
    Returns a DataFrame with results.
    """
    results = []
    for p in prices:
        effect_data = transaction_effect(Decimal(str(p)), Decimal(str(tax_rate)))
        # Add last digit of the total (before rounding) for analysis
        total_str = f"{effect_data['total']:.2f}"
        last_digit = int(total_str[-1])

        results.append({
            'price': float(effect_data['price']),
            'tax': float(effect_data['tax']),
            'total': float(effect_data['total']),
            'rounded': float(effect_data['rounded']),
            'effect': float(effect_data['effect']),
            'last_digit': last_digit
        })
    return pd.DataFrame(results)

def run_monte_carlo(n_transactions, tax_rate, distribution='realistic', price_range=(0.01, 100.0)):
    """
    Generates synthetic purchases and calculates impact.
    """
    if distribution == 'uniform':
        prices = np.random.uniform(price_range[0], price_range[1], n_transactions)
    elif distribution == 'realistic':
        # More small purchases, fewer large ones, and a bias towards .99 endings
        prices = np.random.exponential(scale=20, size=n_transactions)
        prices = np.clip(prices, price_range[0], price_range[1])
        # Add .99 bias: 70% of prices end in .99
        mask = np.random.random(n_transactions) < 0.7
        prices[mask] = np.floor(prices[mask]) + 0.99
    else: # custom or simple random
        prices = np.random.random(n_transactions) * (price_range[1] - price_range[0]) + price_range[0]

    return run_simulation(prices, tax_rate)
