"""
3. Decryption. Decrypts the recived message.

3.1 Uses the private key (p, q) to determine the 4 square roots m1, m2, m3, m4 of c modulo n.
3.2 Decides which one of the 4 messages m1, m2, m3, m4 is the one encrypted.

Here we resolve the 4-to-1 ambiguity by using redundancy:
we only accept blocks whose first character is ' ' (space).
"""

ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
val_to_char = {i: ch for i, ch in enumerate(ALPHABET)}

# ---------- block decoding utilities ----------

def max_block_len(n: int) -> int:
    """
    Same function as in encryption:
    largest L such that 27^L <= n - 1.
    """
    l = 0
    v = 1
    while v * 27 <= n - 1:
        v *= 27
        l += 1
    return l

def int_to_block(m: int, block_len: int) -> str:
    """
    Decode integer m (base 27) back to a block of length block_len.
    """
    digits = []
    for _ in range(block_len):
        digits.append(m % 27)
        m //= 27
    if m != 0:
        raise ValueError("Integer too large for this block length.")
    digits.reverse()
    return "".join(val_to_char[d] for d in digits)

# ---------- number theory utilities ----------

def egcd(a: int, b: int):
    """
    Extended Euclidean algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

# ---------- Rabin decryption ----------

def decrypt_rabin(ciphertext_blocks, n: int, p: int, q: int) -> str:
    """
    Decrypts a list of ciphertext integers using private key (p, q).

    Uses CRT to find 4 square roots for each block and selects the one
    whose decoded block starts with a ' ' (space).
    """
    if n != p * q:
        raise ValueError("Inconsistent keys: n must equal p * q.")

    g, yp, yq = egcd(p, q)
    if g != 1:
        raise ValueError("p and q must be coprime.")

    block_len = max_block_len(n)
    result_chunks = []

    for c in ciphertext_blocks:
        if c < 0 or c >= n:
            raise ValueError("Ciphertext block out of range.")

        # square roots modulo p and q (Rabin special case p ≡ q ≡ 3 mod 4)
        mp = pow(c, (p + 1) // 4, p)
        mq = pow(c, (q + 1) // 4, q)

        # Chinese Remainder Theorem – 4 roots
        r1 = (yp * p * mq + yq * q * mp) % n
        r2 = (-r1) % n
        r3 = (yp * p * mq - yq * q * mp) % n
        r4 = (-r3) % n
        roots = [r1, r2, r3, r4]

        chosen_block = None
        for r in roots:
            try:
                candidate = int_to_block(r, block_len)
            except ValueError:
                continue
            if candidate[0] == " ":  # check redundancy
                chosen_block = candidate
                break

        if chosen_block is None:
            raise ValueError("Failed to find a valid plaintext block.")

        result_chunks.append(chosen_block[1:])  # drop leading space

    return "".join(result_chunks).rstrip()

# ---------- CLI ----------

def main():
    print("=== Rabin Decryption ===")
    n = int(input("Enter public key n: ").strip())
    p = int(input("Enter private key p: ").strip())
    q = int(input("Enter private key q: ").strip())

    line = input("Enter ciphertext blocks (space-separated integers): ").strip()
    if not line:
        print("No ciphertext given.")
        return
    ciphertext_blocks = [int(x) for x in line.split()]

    plaintext = decrypt_rabin(ciphertext_blocks, n, p, q)
    print("\nDecryption done.")
    print("Recovered plaintext:")
    print(plaintext)


if __name__ == "__main__":
    main()