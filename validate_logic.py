from decimal import Decimal
from utils.rounding import nickel_round, transaction_effect
from utils.tax_rates import load_florida_tax_rates

def test_nickel_round():
    assert nickel_round(Decimal('1.00')) == Decimal('1.00')
    assert nickel_round(Decimal('1.01')) == Decimal('1.00')
    assert nickel_round(Decimal('1.02')) == Decimal('1.00')
    assert nickel_round(Decimal('1.03')) == Decimal('1.05')
    assert nickel_round(Decimal('1.04')) == Decimal('1.05')
    assert nickel_round(Decimal('1.05')) == Decimal('1.05')
    assert nickel_round(Decimal('1.06')) == Decimal('1.05')
    assert nickel_round(Decimal('1.07')) == Decimal('1.05')
    assert nickel_round(Decimal('1.08')) == Decimal('1.10')
    assert nickel_round(Decimal('1.09')) == Decimal('1.10')
    print("Nickel rounding tests passed!")

def test_transaction_effect():
    # 9.99 + 7.5% tax (0.74925 -> 0.75) = 10.74. Rounded to 10.75. Effect = +0.01
    res = transaction_effect(Decimal('9.99'), Decimal('0.075'))
    assert res['tax'] == Decimal('0.75')
    assert res['total'] == Decimal('10.74')
    assert res['rounded'] == Decimal('10.75')
    assert res['effect'] == Decimal('0.01')
    print("Transaction effect tests passed!")

def test_data_loading():
    df = load_florida_tax_rates()
    assert not df.empty
    assert 'County' in df.columns
    assert 'TaxRate' in df.columns
    print("Data loading tests passed!")

if __name__ == "__main__":
    test_nickel_round()
    test_transaction_effect()
    test_data_loading()
