import math

def prime_check(num):
    """small prime check utility"""
    if num == 2:
        return True
    if num % 2 == 0 or num < 2:
        return False

    lt = int(math.floor(math.sqrt(num)) + 1)
    for i in range(3, lt, 2):
        if num % i == 0:
            return False

    return True