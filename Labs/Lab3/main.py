import random

def is_probable_prime(n: int, k: int = 10) -> bool:

    # Handle small n explicitly
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Step 0: write n-1 = 2^s * t
    t = n - 1
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(k):
        # Step 1: choose a random a in (1, n)
        a = random.randrange(2, n - 1)

        # Step 2: compute the sequence
        x = pow(a, t, n)   # a^t mod n - implemented in python

        # Step 3:
        if x == 1 or x == n - 1:
            # if first term is 1 => probably prime
            # if first term is -1 => second term is 1 => probably prime
            continue

        composite_for_this_a = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                # this term is -1 => next term is 1 => probably prime
                composite_for_this_a = False
                break

        # Step 4: the algorithm stops
        if composite_for_this_a:
            return False
    return True

if __name__ == "__main__":
    test_numbers = [17, 18, 19, 20, 561, 1105, 1729, 7919]
    for number in test_numbers:
        result = is_probable_prime(number)
        print(f"{number} - {'probably prime' if result else 'composite'}")
