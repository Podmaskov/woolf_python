from random import randint

def get_numbers_ticket(min, max, quantity):
    if min < 1 or max > 1000 or quantity < 1 or quantity > 1000:
        raise ValueError("min must be >= 1, max must be <= 1000, and quantity must be between 1 and 1000")

    if quantity > (max - min + 1):
        raise ValueError("quantity must not exceed the number of possible unique numbers in the range")

    numbers = set()
    while len(numbers) < quantity:
        numbers.add(randint(min, max))

    return list(numbers)

print(get_numbers_ticket(1, 3, 8))