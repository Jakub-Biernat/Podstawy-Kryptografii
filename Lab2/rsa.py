import random
import sys
import math

def is_prime(a):
    if a < 2:
        return False

    for i in range(2, int(math.sqrt(a)) + 1):
        if a % i == 0:
            return False

    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1
        if is_prime(n):
            return n

def rsa(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(1, phi - 1)
    while (math.gcd(e, phi) != 1):
        e = random.randint(1, phi - 1)

    d = pow(e, -1, phi)

    return (e, n), (d, n)

def rsa_cipher(text, public_key):
    ciphertext = []
    e = public_key[0]
    n = public_key[1]
    with open(text, 'r') as file:
        while True:
            character = file.read(1)
            if not character:
                break
            ciphertext.append(ord(character))
        file.close()

    encrypted = [pow(char, e, n) for char in ciphertext]
    print("Tekst zaszyfrowany:")
    print(encrypted)

    return encrypted

def rsa_decipher(encrypted, private_key):
    d = private_key[0]
    n = private_key[1]
    text = [chr(pow(char, d, n)) for char in encrypted]
    result = "".join(text)
    print("Tekst odszyfrowany: ")
    print(result)


def main():
    print()
    bit_num = int(sys.argv[1])
    text = sys.argv[2]

    p = generate_prime(bit_num)
    q = generate_prime(bit_num)
    print("p: " + str(p))
    print("q: " + str(q))
    print()

    public_key, private_key = rsa(p, q)
    print("Klucz publiczny: " + str(public_key))
    print("Klucz prywatny: " + str(private_key))
    print()

    cipher = rsa_cipher(text, public_key)
    print()
    rsa_decipher(cipher, private_key)
    print()
    

main()