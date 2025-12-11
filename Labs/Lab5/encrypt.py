import json
from paillier_utils import encrypt_text

def main():
    # Load public key
    try:
        with open("public_key.json", "r") as f:
            pk = json.load(f)
        n = int(pk["n"])
        g = int(pk["g"])
        public_key = (n, g)
    except Exception as e:
        print("Error loading public_key.json:", e)
        return

    plaintext = input("Enter plaintext (space and A-Z only): ")

    try:
        cipher_blocks = encrypt_text(plaintext, public_key)
    except ValueError as e:
        print("Error in plaintext validation/encryption:", e)
        return

    ciphertext_file = input("Ciphertext output file (default: ciphertext.txt): ").strip()
    if not ciphertext_file:
        ciphertext_file = "ciphertext.txt"

    try:
        with open(ciphertext_file, "w", encoding="utf-8") as f:
            # space-separated integers on one line
            f.write(" ".join(str(c) for c in cipher_blocks))
    except Exception as e:
        print("Error writing ciphertext file:", e)
        return

    print("\nEncryption done.")
    print(f"Ciphertext saved to: {ciphertext_file}")

if __name__ == "__main__":
    main()