import sys
from Crypto.Util import number

PRIME_BITS = 32

def split_shares_shamirs(n, p, t, s):
    coeffs = [s] + [number.getRandomRange(1, p - 1) for _ in range(t-1)]
    for coeff in coeffs:
        print(f"Wygenerowany coeff: {coeff}")

def join_shares(shares, k):
    sum_shares = sum(shares)
    s = sum_shares % k
    return s

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

    split_shares_shamirs(n, p, t, s)

