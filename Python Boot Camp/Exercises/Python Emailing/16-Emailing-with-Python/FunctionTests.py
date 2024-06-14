def fibonacci_sequence(limit):
    """
    A generator function that yields the first `limit` Fibonacci numbers.

    Args:
    limit (int): The number of Fibonacci numbers to generate.

    Yields:
    int: The next Fibonacci number in the sequence.
    """
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b

# Example usage:
for fib_num in fibonacci_sequence(10):
    print(fib_num)
