import random
import time

# Euclidean Algorithm
def euclid(a, b):
    while b:
        a, b = b, a % b # a <- b, b <- a mod b
    return a

# Subtraction-based Algorithm
def subtraction(a, b):
    if a == 0 or b == 0:
        return a + b
    while a != b:
        # subtract the smaller number from the larger one
        if a > b:
            a -= b
        else:
            b -= a
    return a # return any of them as they are equal now

# in Python int can handle arbitrary large integers, so no special handling is needed
# Binary GCD (Stein’s Algorithm) – works efficiently for very large numbers
def Stein(a, b):
    # if either number is zero, the gcd is the other number
    if a == 0: return b
    if b == 0: return a

    # Find common factors of 2
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1

    # if a is even, remove all factors of 2 from a
    while (a & 1) == 0:
        a >>= 1

    while b != 0:
        # if b is even, remove all factors of 2 from b
        while (b & 1) == 0:
            b >>= 1

        # continue the subtraction step
        if a > b:
            a, b = b, a - b
        else:
            b -= a

    # Restore common factors of 2
    return a << shift


# Runtime Comparison
def compare_algorithms(test_cases):
    # Writing results in microseconds for easier comparison
    # (for small numbers, the time taken will be very small)
    print("Comparing GCD Algorithms Runtime (in microseconds):")
    print(f"{'a':>12} {'b':>12} | {'Euclidean':>18} {'Subtraction':>18} {'Binary':>15}")
    print("-" * 81)

    for (a, b) in test_cases:
        # Euclidean
        start = time.perf_counter() # start timer
        euclid(a, b)
        t1 = (time.perf_counter() - start) * 1_000_000 # stop timer and compute time taken
        # perf_counter() returns time in seconds, we are multiplying by 1_000_000 to convert to microseconds

        # Subtraction
        start = time.perf_counter()
        subtraction(a, b)
        t2 = (time.perf_counter() - start) * 1_000_000

        # Stein
        start = time.perf_counter()
        Stein(a, b)
        t3 = (time.perf_counter() - start) * 1_000_000

        print(f"{a:12d} {b:12d} | {t1:18.2f} {t2:18.2f} {t3:15.2f}")


# 10 test cases including small, medium, and large numbers
test_cases = [
    (0, 18),
    (100, 25),
    (270, 192),
    (1000, 10),
    (99991, 99989), # large coprime numbers
    (2**20, 2**15), # powers of two
    (123456, 789012), # random large numbers
    (982451653, 57885161), # large primes
    (2**32 - 1, 2**30 - 1), # Mersenne primes
    (random.getrandbits(200), random.getrandbits(200))  # very large integers
]

if __name__ == "__main__":
    compare_algorithms(test_cases)