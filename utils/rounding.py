from decimal import Decimal, ROUND_HALF_UP

def nickel_round(amount: Decimal) -> Decimal:
    """
    Rounds a Decimal amount to the nearest nickel (0.05).
    Uses ROUND_HALF_UP for the 0.025 cases if they occur,
    though typically it's nearest.
    """
    # amount * 20 -> round to nearest integer -> divide by 20
    return (amount * Decimal('20')).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / Decimal('20')

def transaction_effect(price: Decimal, tax_rate: Decimal) -> dict:
    """
    Calculates the tax, total, rounded total, and the rounding effect.
    tax_rate should be a decimal (e.g., 0.07 for 7%).
    """
    tax = (price * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total = price + tax
    rounded = nickel_round(total)
    effect = rounded - total

    return {
        'price': price,
        'tax': tax,
        'total': total,
        'rounded': rounded,
        'effect': effect
    }
