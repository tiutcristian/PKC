# Paillier Cryptosystem

## 1. Overview

The **Paillier cryptosystem** is a public-key (asymmetric) encryption scheme based on the hardness of computing discrete logarithms modulo composite integers. It is additively **homomorphic**: from encryptions of two messages you can obtain an encryption of their sum without knowing the secret key.

This project implements Paillier with a small custom alphabet and simple command-line interaction.

---

## 2. Mathematical Background

### 2.1 Key Generation

1. Choose two large random primes `p` and `q`.
2. Compute:
   - $n = p \cdot q$
   - $\lambda = lcm(p-1, q-1)$
3. Choose $g$ in $ℤ^*_{n²}$. In practice we pick $g = n + 1$, which simplifies the math.
4. Compute:  
   - $\mu = (L(g^\lambda \mod n^2))^{-1} \mod n$
5. Keys:
   - **Public key**: $(n, g)$
   - **Private key**: $(\lambda, \mu)$

### 2.2 Encryption

To encrypt a message $m$ with $0 \le m < n$:

1. Pick a random $r$ in $\{1, …, n−1\}$ such that $gcd(r, n) = 1$.
2. Compute the ciphertext:
   - $c = g^m · r^n \mod n^2$
   

### 2.3 Decryption

Given ciphertext $c$ and private key $(\lambda, \mu, n)$:

1. Compute: 
   - $x = c^\lambda \mod n^2$.
2. Compute
   - $L(x) = \frac{x - 1}{n}$.
3. Recover:
   - $m = L(x) \cdot \mu \mod n$

---

## 3. Alphabet and Message Encoding

We use an alphabet of **27 characters**:

- The space `" "` (blank)
- The 26 uppercase letters: `A–Z`

Internally we map:

- `" "` → 0  
- `"A"` → 1  
- `"B"` → 2  
- …  
- `"Z"` → 26  

Each character is encoded as a number in $\{0, …, 26\}$ and encrypted **individually**. For a plaintext string, we get a list of small integers; the script encrypts each one separately and returns a list of ciphertext integers.

---

## 4. Plaintext & Ciphertext Validation

### 4.1 Plaintext Validation

- Only characters in the allowed alphabet are accepted: space and `A–Z`.
- Plaintext is converted to uppercase before encoding.
- If any other character is encountered, an error is raised.

### 4.2 Ciphertext Validation

- Ciphertext is represented as a list of integers.
- Each integer must be in the range $[0, n^2 − 1]$.
- Parsing errors or out-of-range values cause validation failure.

---

## 5. Usage

### Typical workflow:
- **Receiver** generates key pair and shares the public key with the sender.
- **Sender** encrypts the plaintext message using the public key and sends the ciphertext to the receiver.
- **Receiver** decrypts the ciphertext using their private key to recover the original plaintext.

### 5.1. Generate keys
    
- The public and private key values are generated and saved to `public_key.json` and `private_key.json`.
   ```shell
    python3 keygen.py
   ```

### 5.2. Encrypt a plaintext
 - Input a string containing only space and A–Z (case-insensitive).
 - The program uses the saved public key to encrypt the message and generates a list of integers as ciphertext.
 - The ciphertext is saved to a file with configurable name (default: `ciphertext.txt`).
    ```shell
     python3 encrypt.py
    ```

### 5.3. Decrypt the ciphertext
 - The program reads the ciphertext from the file and uses the saved private key to decrypt it back to plaintext. 
 - The result is printed to the console.
    ```shell
     python3 decrypt.py
    ```

