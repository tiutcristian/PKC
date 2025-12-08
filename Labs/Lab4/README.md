# Rabin Cryptosystem (27-char alphabet)

This project implements the **Rabin public-key cryptosystem** over a custom alphabet of `" SPACE + A–Z "` (27 characters). The system is split into three standalone programs:

- `keygen.py` – key generation (Receiver)
- `encrypt.py` – encryption (Sender)
- `decrypt.py` – decryption (Receiver)

---

## Alphabet & Encoding

- Allowed characters:  
  `␣` (space), `A B C ... Z`
- Text is converted to **base-27** numbers and processed in fixed-size blocks.
- Each block reserves its **first character as a space** (`' '`) to add redundancy.  
  This is used during decryption to pick the correct root among the 4 Rabin roots.

---

## 1. Key Generation – `keygen.py`

Receiver runs:

```bash
  python keygen.py
```

Steps:

1. Generates two random large primes `p` and `q` such that `p ≡ q ≡ 3 (mod 4)`.
2. Computes `n = p * q`.
3. Prints:
   - **Public key:** `n`
   - **Private key:** `p`, `q`

Receiver shares **only `n`** with Sender and keeps `p` and `q` secret.

---

## 2. Encryption – `encrypt.py`

Sender runs:

```bash
  python encrypt.py
```

Steps:

1. Inputs Receiver’s public key `n`.
2. Inputs a plaintext (only space and `A–Z`).
3. Program:
   - Encodes the text into blocks (integers `< n`).
   - Encrypts each block as `c = m² mod n`.
4. Outputs:
   - Block length used.
   - Ciphertext as a space-separated list of integers.

Sender sends this ciphertext line to Receiver.

---

## 3. Decryption – `decrypt.py`

Receiver runs:

```bash
  python decrypt.py
```

Steps:

1. Inputs:
   - `n` (public key)
   - `p`, `q` (private key)
2. Pastes the ciphertext blocks (space-separated integers).
3. Program:
   - Uses `(p, q)` to compute the **4 square roots** for each block via CRT.
   - Keeps only the root whose decoded block starts with a space (`' '`).
   - Reassembles all blocks into the original plaintext.

Outputs the recovered message.

---

## Notes

- Security relies on the hardness of factoring `n`: without `p` and `q`, computing modular square roots (`m` from `c = m² mod n`) is believed hard.
- The implementation is for educational purposes and uses relatively small key sizes by default; do **not** use as-is for real security.