import json
from paillier_utils import decrypt_text

def main():
    # Load private key
    try:
        with open("private_key.json", "r") as f:
            sk = json.load(f)
        lam = int(sk["lambda"])
        mu = int(sk["mu"])
        n = int(sk["n"])
        private_key = (lam, mu, n)
    except Exception as e:
        print("Error loading private_key.json:", e)
        return

    ciphertext_file = input("Ciphertext file (default: ciphertext.txt): ").strip()
    if not ciphertext_file:
        ciphertext_file = "ciphertext.txt"

    try:
        with open(ciphertext_file, "r", encoding="utf-8") as f:
            raw = f.read().strip()
    except Exception as e:
        print("Error reading ciphertext file:", e)
        return

    if not raw:
        print("Ciphertext file is empty.")
        return

    try:
        cipher_blocks = [int(x) for x in raw.split()]
    except ValueError:
        print("Ciphertext file must contain integers separated by spaces.")
        return

    try:
        plaintext = decrypt_text(cipher_blocks, private_key)
    except ValueError as e:
        print("Error during decryption:", e)
        return

    print("\nDecryption done.")
    print("Decrypted plaintext:")
    print(f"\033[92m{plaintext}\033[0m")

if __name__ == "__main__":
    main()