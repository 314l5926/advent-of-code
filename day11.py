from functools import lru_cache
from math import log10, floor

@lru_cache(maxsize=None)
def count_numbers(num, iterations):
    """Count how many numbers will be generated after given iterations."""
    if iterations == 0:
        return 1

    # Get number of digits
    num_digits = floor(log10(num)) + 1 if num > 0 else 1

    if num == 0:
        # Rule 1: 0 becomes 1
        return count_numbers(1, iterations - 1)
    elif num_digits % 2 == 0:
        # Rule 2: Split number with even digits
        divisor = 10 ** (num_digits // 2)
        left = num // divisor
        right = num % divisor
        return count_numbers(left, iterations - 1) + count_numbers(right, iterations - 1)
    else:
        # Rule 3: Multiply by 2024
        return count_numbers(num * 2024, iterations - 1)

# Example usage
def count_sequence(initial_numbers, iterations):
    """Count total numbers after iterations starting from initial list."""
    return sum(count_numbers(num, iterations) for num in initial_numbers)


