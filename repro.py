from decimal import Decimal, ROUND_HALF_UP

def nickel_round(amount: Decimal) -> Decimal:
    return (amount * Decimal('20')).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / Decimal('20')

def transaction_effect(price: Decimal, tax_rate: Decimal) -> dict:
    tax = (price * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total = price + tax
    rounded = nickel_round(total)
    effect = rounded - total
    return {'price': price, 'tax': tax, 'total': total, 'rounded': rounded, 'effect': effect}

# .99 prices with 7% tax
tr = Decimal('0.07')
for i in range(1, 11):
    p = Decimal(str(i)) + Decimal('0.99')
    res = transaction_effect(p, tr)
    print(f"P: {p}, Tax: {res['tax']}, Total: {res['total']}, Rounded: {res['rounded']}, Effect: {res['effect']}")
