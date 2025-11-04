def extended_gcd(a, b):
    # a*x + b*y = g = gcd(a, b)
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a, n):
    # a^(-1) mod n
    g, x, _ = extended_gcd(a, n)
    if g != 1: # No modular inverse if a and n are not coprime
        raise ValueError(f"No modular inverse for {a} mod {n}")
    return x % n


def solve_congruences(a_list, n_list):
    # Solve system x ≡ a_i (mod n_i)
    N = 1
    for n in n_list:
        N *= n

    result = 0
    for a_i, n_i in zip(a_list, n_list):
        N_i = N // n_i
        M_i = mod_inverse(N_i, n_i)
        result += a_i * N_i * M_i

    return result % N, N


if __name__ == "__main__":
    """
        x ≡ 2 (mod 3)
        x ≡ 3 (mod 4)
        x ≡ 1 (mod 5)
    """
    a = [2, 3, 1]
    n = [3, 4, 5]
    x, N = solve_congruences(a, n)
    print(f"x ≡ {x} (mod {N})")