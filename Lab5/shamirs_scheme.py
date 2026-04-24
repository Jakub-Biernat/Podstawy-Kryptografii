import sys
from Crypto.Util import number

PRIME_BITS = 32

def split_shares_shamirs(n, p, t, s):
    coeffs = [number.getRandomRange(1, p - 1) for _ in range(t-1)]
    shares = []

    for x in range(1, n + 1):
        s_i = s
        for j, coeff_j in enumerate(coeffs):
            s_i += coeff_j * x ** (j + 1)

        s_i = s_i % p
        shares.append((x, s_i))

    return shares

def join_shares_shamirs(shares, p):
    s = 0

    for i, (xi, yi) in enumerate(shares):
        numerator = 1
        denominator = 1

        for j, (xj, _) in enumerate(shares):
            if i != j:
                numerator = (numerator * (-xj)) % p
                denominator = (denominator * (xi - xj)) % p

        lagrange = numerator * pow(denominator, -1, p)

        s = (s + yi * lagrange) % p

    return s

def print_shares(shares, text_before):
    print(text_before)
    for i, share in enumerate(shares):
        print(f"Udzial {i + 1}: {share}")

if __name__ == '__main__':
    #Wywołanie: py ./shamirs_scheme n t
    n = int(sys.argv[1])
    t = int(sys.argv[2])
    p = number.getPrime(PRIME_BITS)
    while p <= n:
        p = number.getPrime(PRIME_BITS)
    s = number.getRandomRange(1, p)

    print("Podzial sekretu Shamira")
    print(f"Wygenerowany sekret: {s}")

    print(f"\nWygenerowana liczba p: {p}")

    shares = split_shares_shamirs(n, p, t, s)
    print_shares(shares, "\nWygenerowane udzialy")

    print("\nGenerowanie sekretu przy użyciu n udziałów")
    recreated_s = join_shares_shamirs(shares, p)
    print(f"Wygenerowany sekret: {recreated_s}")

    print("\nGenerowanie sekretu przy użyciu t udziałów")
    sub_shares = shares.copy()
    while len(sub_shares) > t:
        index_to_pop = number.getRandomRange(0, len(sub_shares))
        sub_shares.pop(index_to_pop)
    print_shares(sub_shares, "Uzyte udzialy:")
    recreated_s = join_shares_shamirs(sub_shares, p)
    print(f"Wygenerowany sekret: {recreated_s}")

    print("\nGenerowanie sekretu przy użyciu t - 1 udziałów")
    sub_shares = shares.copy()
    while len(sub_shares) > t - 1:
        index_to_pop = number.getRandomRange(0, len(sub_shares))
        sub_shares.pop(index_to_pop)
    print_shares(sub_shares, "Uzyte udzialy:")
    recreated_s = join_shares_shamirs(sub_shares, p)
    print(f"Wygenerowany sekret: {recreated_s}")

    #Jaka jest minimalna, wymagana liczba udziałów aby algorytm działał poprawnie?
    #2, ponieważ dla t = 1 wartość udziału będzie równa wartości sekretu

