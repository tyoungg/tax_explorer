import pandas as pd
import os
from decimal import Decimal

def load_florida_tax_rates():
    """Reads Florida tax rates from the data directory."""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'florida_tax_rates.csv')
    df = pd.read_csv(data_path)
    # Ensure TaxRate is treated as Decimal for precision
    df['TaxRate'] = df['TaxRate'].apply(lambda x: Decimal(str(x)))
    return df

def get_county_rate(county_name):
    df = load_florida_tax_rates()
    rate = df[df['County'] == county_name]['TaxRate'].iloc[0]
    return rate
