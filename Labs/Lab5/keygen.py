import json
from paillier_utils import generate_keypair

def main():
    bits_str = input("Key size in bits (e.g. 256): ").strip()
    try:
        bits = int(bits_str) if bits_str else 256
    except ValueError:
        print("Invalid input, using 256 bits.")
        bits = 256

    print("Generating keys...")
    public_key, private_key = generate_keypair(bits)

    n, g = public_key
    lam, mu, n_priv = private_key

    # Save to JSON files
    with open("public_key.json", "w") as f:
        json.dump({"n": n, "g": g}, f)

    with open("private_key.json", "w") as f:
        json.dump({"lambda": lam, "mu": mu, "n": n_priv}, f)

    print("\nKeys generated and saved:")
    print("  public_key.json")
    print("  private_key.json")

if __name__ == "__main__":
    main()