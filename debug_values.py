from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

def nickel_round(amount: Decimal) -> Decimal:
    return (amount * Decimal('20')).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / Decimal('20')

def transaction_effect(price: Decimal, tax_rate: Decimal) -> dict:
    tax = (price * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total = price + tax
    rounded = nickel_round(total)
    effect = rounded - total
    return {'effect': effect}

prices = [Decimal(str(i)) + Decimal('0.99') for i in range(1, 101)]
tr = Decimal('0.07')
effects = [transaction_effect(p, tr)['effect'] for p in prices]
print(f"7.0% tr, .99 prices: Avg Bias = {sum(effects)/len(effects)}")

tr = Decimal('0.075')
effects = [transaction_effect(p, tr)['effect'] for p in prices]
print(f"7.5% tr, .99 prices: Avg Bias = {sum(effects)/len(effects)}")
