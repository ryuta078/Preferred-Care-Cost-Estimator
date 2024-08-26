def round_half_even(n):
    integer_part = int(n)
    decimal_part = n - integer_part

    if decimal_part > 0.5 or (decimal_part == 0.5 and integer_part % 2 != 0):
        return integer_part + 1
    else:
        return integer_part

def calculate_medical_points(price, conversion_rate=10):
    if price is None:
        return None

    rounded_price = round_half_even(price)
    points = rounded_price / conversion_rate

    return points
