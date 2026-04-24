import sys
from Crypto.Util import number

PRIME_BITS = 32

def split_shares_shamirs(n, p, t, s):
    coeffs = [s] + [number.getRandomRange(1, p - 1) for _ in range(t-1)]
    shares = []

    for x in range(1, n + 1):
        s_i = 0
        for j, coeff_j in enumerate(coeffs):
            s_i += coeff_j * x ** j

        s_i = s_i % p
        shares.append((x, s_i))

    return shares

def join_shares_shamirs(shares, p):
    s = 0

    for i, share in enumerate(shares):

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

    print("\nWygenerowane udzialy:")
    shares = split_shares_shamirs(n, p, t, s)
    for i, share in enumerate(shares):
        print(f"Udzial {i + 1}: {share}")

