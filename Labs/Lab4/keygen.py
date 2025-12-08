"""
1. Key generation. Create a public key and a private key.

1.1 Generates 2 random large distinct primes p, q of approximately same size.
1.2 Computes n = p * q.
1.3 Public key is n; Private key is (p, q).
"""

import secrets
import random

# ---------- Number theory utilities ----------

def is_probable_prime(n: int, k: int = 8) -> bool:
    """
    Miller–Rabin primality test (probabilistic) for odd n >= 3.
    """
    if n < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    """
    Generate a random prime p of the given bit size with p ≡ 3 (mod 4).
    """
    while True:
        candidate = secrets.randbits(bits) | 1 | (1 << (bits - 1))
        candidate += (3 - candidate) % 4  # force ≡ 3 (mod 4)
        if is_probable_prime(candidate):
            return candidate


def generate_keypair(bits: int = 64):
    """
    Generate Rabin key pair.

    bits ~ size of n. p and q will each be about bits/2.
    """
    if bits < 16:
        raise ValueError("Use at least 16 bits for the modulus.")
    half = bits // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while p == q:
        q = generate_prime(half)
    n = p * q
    return n, p, q


def main():
    print("=== Rabin Key Generation ===")
    try:
        bits = int(input("Desired bit-length for n (e.g., 64, 128): ").strip() or "64")
    except ValueError:
        bits = 64

    n, p, q = generate_keypair(bits)

    print("\nKeys generated:")
    print(f"Public key n = {n}")
    print(f"Private key p = {p}")
    print(f"Private key q = {q}")
    print("\nDistribute n (public key).")
    print("Keep p and q secret.")


if __name__ == "__main__":
    main()