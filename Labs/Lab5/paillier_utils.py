import secrets
import math
from typing import List, Tuple

# =========================
#  Alphabet and encoding
# =========================

ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 27 characters: space + A-Z
CHAR_TO_VAL = {c: i for i, c in enumerate(ALPHABET)}
VAL_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}


def text_to_ints(text: str) -> List[int]:
    """
    Convert plaintext (string) to list of integers in [0, 26].
    Validates that only allowed characters are present.
    """
    text = text.upper()
    result = []
    for ch in text:
        if ch not in CHAR_TO_VAL:
            raise ValueError(
                f"Invalid character '{ch}'. Allowed: space and A-Z."
            )
        result.append(CHAR_TO_VAL[ch])
    return result


def ints_to_text(vals: List[int]) -> str:
    """
    Convert list of integers (0-26) back to plaintext string.
    """
    try:
        return "".join(VAL_TO_CHAR[v] for v in vals)
    except KeyError as e:
        raise ValueError(f"Invalid symbol value in decrypted data: {e}")


# =========================
#  Number theory helpers
# =========================

def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm.
    Returns (g, x, y) with g = gcd(a, b) and x*a + y*b = g.
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def modinv(a: int, m: int) -> int:
    """
    Modular inverse: return x such that (a * x) % m == 1.
    Raises ValueError if inverse does not exist.
    """
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def is_probable_prime(n: int, k: int = 20) -> bool:
    """
    Miller-Rabin primality test (probabilistic).
    Suitable for toy key generation.
    """
    if n < 2:
        return False

    # Small prime trial division first
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False

    # Write n-1 as 2^r * d
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # random in [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime(bits: int) -> int:
    """
    Generate a probable prime with given bit length.
    """
    if bits < 2:
        raise ValueError("Bit length must be >= 2")
    while True:
        candidate = secrets.randbits(bits)
        # Ensure the candidate has the correct bit length and is odd
        candidate |= (1 << (bits - 1))  # set highest bit
        candidate |= 1                   # make it odd
        if is_probable_prime(candidate):
            return candidate


# =========================
#  Paillier key generation
# =========================

def generate_keypair(bits: int = 256):
    """
    Generate Paillier public and private keys.
    bits = total bit length of n (approximately).
    Returns:
      public_key = (n, g)
      private_key = (lambda, mu, n)
    """
    half = bits // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while q == p:
        q = generate_prime(half)

    n = p * q
    lam = lcm(p - 1, q - 1)
    g = n + 1  # standard choice that simplifies calculations
    n2 = n * n

    # Compute mu = (L(g^lambda mod n^2))^-1 mod n
    x = pow(g, lam, n2)
    L = (x - 1) // n
    mu = modinv(L, n)

    public_key = (n, g)
    private_key = (lam, mu, n)
    return public_key, private_key


# =========================
#  Paillier encryption / decryption
# =========================

def encrypt_symbol(m: int, public_key) -> int:
    """
    Encrypt a single symbol m in [0, n-1].
    Returns ciphertext c in [0, n^2 - 1].
    """
    n, g = public_key
    n2 = n * n
    if not (0 <= m < n):
        raise ValueError("Message symbol out of range for modulus n.")

    # Choose random r in [1, n-1] with gcd(r, n) = 1
    while True:
        r = secrets.randbelow(n)
        if r > 0 and math.gcd(r, n) == 1:
            break

    c = (pow(g, m, n2) * pow(r, n, n2)) % n2
    return c


def decrypt_symbol(c: int, private_key) -> int:
    """
    Decrypt a single ciphertext c.
    Returns m in [0, n-1].
    """
    lam, mu, n = private_key
    n2 = n * n

    if not (0 <= c < n2):
        raise ValueError("Ciphertext block out of range for modulus n^2.")

    x = pow(c, lam, n2)
    L = (x - 1) // n
    m = (L * mu) % n
    return m


def encrypt_text(plaintext: str, public_key) -> List[int]:
    """
    Encrypt a whole plaintext string.
    Returns a list of integer ciphertext blocks.
    """
    symbols = text_to_ints(plaintext)  # validates plaintext
    return [encrypt_symbol(m, public_key) for m in symbols]


def decrypt_text(cipher_blocks: List[int], private_key) -> str:
    """
    Decrypt a list of ciphertext blocks back to plaintext string.
    """
    symbols = [decrypt_symbol(c, private_key) for c in cipher_blocks]
    return ints_to_text(symbols)