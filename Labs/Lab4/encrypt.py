"""
2. Encryption. Sends an encrypted message.

2.1 Get the public key n.
2.2 Represents the message as a number m between 0 and n - 1.
2.3 Computes c = m^2 mod n.
2.4 Sends the ciphertext c.
"""

# Alphabet: 27 characters = ' ' + 'A'..'Z'
ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
char_to_val = {ch: i for i, ch in enumerate(ALPHABET)}

def max_block_len(n: int) -> int:
    """
    Largest L such that 27^L <= n - 1.
    We use blocks of length L characters.
    """
    l = 0
    v = 1
    while v * 27 <= n - 1:
        v *= 27
        l += 1
    return l

def block_to_int(block: str) -> int:
    """
    Encode a fixed-length block to an integer in base 27.
    """
    m = 0
    for ch in block:
        m = m * 27 + char_to_val[ch]
    return m

def encode_text(plaintext: str, n: int):
    """
    Validate and encode plaintext into a list of integers.

    Redundancy: first character in each block is a known ' ' (space)
    to help resolve the 4-to-1 ambiguity on decryption.
    """
    plaintext = plaintext.upper()
    for ch in plaintext:
        if ch not in ALPHABET:
            raise ValueError(f"Invalid character in plaintext: {repr(ch)}")

    block_len = max_block_len(n)
    if block_len <= 1:
        raise ValueError("Modulus too small for this alphabet.")

    payload_len = block_len - 1  # first char is redundant space
    blocks = []

    for i in range(0, len(plaintext), payload_len):
        chunk = plaintext[i : i + payload_len]
        block_str = " " + chunk.ljust(payload_len)  # pad with spaces
        blocks.append(block_str)

    block_ints = [block_to_int(b) for b in blocks]
    return block_ints, block_len

def encrypt_blocks(block_ints, n: int):
    """
    Rabin encryption: c = m^2 mod n for each block.
    """
    return [pow(m, 2, n) for m in block_ints]

def main():
    print("=== Rabin Encryption ===")
    n = int(input("Enter public key n: ").strip())

    plaintext = input("Enter plaintext (allowed: space and A-Z): ")
    block_ints, block_len = encode_text(plaintext, n)
    ciphertext_blocks = encrypt_blocks(block_ints, n)

    print("\nEncryption done.")
    print(f"Block length used (characters per block) = {block_len}")
    print("\nCiphertext blocks (integers):")
    print(ciphertext_blocks)
    print("\nSend the following line as the ciphertext:")
    print(" ".join(str(c) for c in ciphertext_blocks))


if __name__ == "__main__":
    main()