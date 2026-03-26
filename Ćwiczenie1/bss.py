import random
import sys
import math


def is_prime(a):
    if a < 2:
        return False

    for i in range(2, a):
        if a % i == 0:
            return False

    return True


def lsb(a):
    return a & 1


def block_to_int(block):
    block = ''.join(str(bit) for bit in block)
    return int(block, 2)


def bbs(p, q, num_of_bits):
    n = p * q
    x = []
    bits = []

    seed = random.randint(1, n - 1)
    while (math.gcd(seed, n) != 1):
        seed = random.randint(1, n - 1)
    print("Ziarno: " + str(seed))

    x.append(pow(seed, 2, n))
    for i in range(1, num_of_bits):
        x.append(pow(x[i - 1], 2, n))

    bits = [lsb(number) for number in x]
    return bits


def test1(bits):
    num_of_ones = 0
    for bit in bits:
        if bit == 1:
            num_of_ones += 1

    if num_of_ones <= 9725 or num_of_ones >= 10275:
        print("Test pojedynczych bitow niezdany, liczba jedynek: " + str(num_of_ones))
    else:
        print("Test pojedynczych bitow zdany, liczba jedynek: " + str(num_of_ones))

    return


def test2(bits):
    series = [[0] * 6 for _ in range(2)]
    act_serie_len = 1
    act_serie_bit = bits[0]

    for bit in bits[1:]:
        if bit == act_serie_bit:
            act_serie_len += 1
        else:
            if act_serie_len >= 6:
                series[act_serie_bit][5] += 1
            else:
                series[act_serie_bit][act_serie_len - 1] += 1
            act_serie_bit = bit
            act_serie_len = 1

    ranges = [
        (2315, 2685),
        (1114, 1386),
        (527, 723),
        (240, 384),
        (103, 209),
        (103, 209)
    ]

    passed = True

    for bit in range(2):
        for length in range(6):
            if not (ranges[length][0] <= series[bit][length] <= ranges[length][1]):
                passed = False

    if passed:
        print("Test serii zdany")
    else:
        print("Test serii niezdany")

    print("Liczba serii zer jedno-znakowych: " + str(series[0][0]))
    print("Liczba serii zer dwu-znakowych: " + str(series[0][1]))
    print("Liczba serii zer trzy-znakowych: " + str(series[0][2]))
    print("Liczba serii zer cztero-znakowych: " + str(series[0][3]))
    print("Liczba serii zer piecio-znakowych: " + str(series[0][4]))
    print("Liczba serii zer ponad piecio-znakowych: " + str(series[0][5]))
    print()
    print("Liczba serii jedynek jedno-znakowych: " + str(series[1][0]))
    print("Liczba serii jedynek dwu-znakowych: " + str(series[1][1]))
    print("Liczba serii jedynek trzy-znakowych: " + str(series[1][2]))
    print("Liczba serii jedynek cztero-znakowych: " + str(series[1][3]))
    print("Liczba serii jedynek piecio-znakowych: " + str(series[1][4]))
    print("Liczba serii jedynek ponad piecio-znakowych: " + str(series[1][5]))


def test3(bits):
    max_serie_len = 1
    act_serie_len = 1
    act_serie_bit = bits[0]

    for bit in bits[1:]:
        if bit == act_serie_bit:
            act_serie_len += 1
        else:
            max_serie_len = max(max_serie_len, act_serie_len)
            act_serie_bit = bit
            act_serie_len = 1

    if max_serie_len >= 26:
        print("Test najdluzszej serii niezdany, dlugosc najdluzszej serii: " + str(max_serie_len))
    else:
        print("Test najdluzszej serii zdany, dlugosc najdluzszej serii: " + str(max_serie_len))


def test4(bits):
    blocks = [bits[i:i + 4] for i in range(0, len(bits), 4)]
    s = [0] * 16

    for block in blocks:
        s[block_to_int(block)] += 1

    x = 16 / 5000 * sum(element ** 2 for element in s) - 5000

    if x <= 2.16 or x >= 46.17:
        print("Test pokerowy niezdany, wartosc X: " + str(x))
    else:
        print("Test pokerowy zdany, wartosc X: " + str(x))


def main():
    p = int(sys.argv[1])
    q = int(sys.argv[2])
    # seed = int(sys.argv[3])

    if not is_prime(p):
        print("p nie jest liczba pierwsza")

    if not is_prime(q):
        print("q nie jest liczba pierwsza")

    if p % 4 != 3:
        print("p mod 4 nie jest rowne 3")

    if q % 4 != 3:
        print("q mod 4 nie jest rowne 3")

    bits = bbs(p, q, 20000)
    test1(bits)
    test2(bits)
    test3(bits)
    test4(bits)


main()