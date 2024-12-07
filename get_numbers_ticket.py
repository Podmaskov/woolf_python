from random import randint

def get_numbers_ticket(min, max, quantity):
    if min < 1 or max > 1000 or quantity < 1 or quantity > 1000:
        raise ValueError("min must be >= 1, max must be <= 1000, and quantity must be between 1 and 1000")
    
    numbers = []
    count = 0
    while count < quantity:
        numbers.append(randint(min, max))
        count += 1
    return numbers

print(get_numbers_ticket(1, 1000, 8))