import sys
from secrets import randbelow

def split_shares(n, k, s):
    shares = [randbelow(k) for _ in range(n - 1)]
    sum_shares = sum(shares)
    s_n = (s - sum_shares) % k
    shares.append(s_n)
    return shares

def join_shares(shares, k):
    sum_shares = sum(shares)
    s = sum_shares % k
    return s

if __name__ == '__main__':
    #Wywołanie: py ./trivial_method n k
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    s = randbelow(k)

    print("Podzial sekretu: metoda trywialna")
    print(f"Wygenerowany sekret: {s}")

    shares = split_shares(n, k, s)
    print("\nFaza podzialu, wygenerowane podzialy: ")
    for i in range(len(shares)):
        print(f"Udzial {i + 1}: {shares[i]}")

    print("\nFaza odtwarzania sekretu")
    recreated_s = join_shares(shares, k)
    print(f"Odtworzony sekret: {recreated_s}")

    print("\nEksperyment: odtwarzanie sekretu bez jednego udzialu")
    pop_index = randbelow(n)
    print(f"Usunięty udzial {pop_index + 1}: {shares.pop(pop_index)}")
    print("Faza odtwarzania sekretu")
    recreated_s = join_shares(shares, k)
    print(f"Odtworzony sekret: {recreated_s}")

