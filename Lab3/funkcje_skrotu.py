import hashlib
from string import ascii_letters, digits
import time
import matplotlib.pyplot as plt
from secrets import choice

ALPHABET = ascii_letters + digits

def generate_hash(text, function):
    hash = hashlib.new(function)
    hash.update(text.encode())
    return hash.hexdigest()

def compare_hashes(texts):
    functions = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']

    input_bits = []
    times = {name: [] for name in functions}
    hash_lengths = {name: [] for name in functions}

    for text in texts:
        input_bits.append(len(text.encode()) * 8)
        for function in functions:
            start = time.perf_counter()
            hash = generate_hash(text, function)
            stop = time.perf_counter()

            times[function].append(stop - start)
            hash_lengths[function].append(len(hash) * 4)

    plt.figure(figsize=(12, 6))

    ax1 = plt.subplot(1, 2, 1)
    for function in functions:
        ax1.plot(input_bits, hash_lengths[function], label=function)

    ax1.set_xlabel("Długość danych wejściowych (bity)")
    ax1.set_ylabel("Długość wygenerowanego hasha (bity)")
    ax1.set_title("Długość hasha w zależności od długości danych")
    ax1.legend()
    ax1.grid()
    ax1.ticklabel_format(style='plain', axis='x')

    ax2 = plt.subplot(1, 2, 2)
    for function in functions:
        ax2.plot(input_bits, times[function], label=function)

    ax2.set_xlabel("Długość danych wejściowych (bity)")
    ax2.set_ylabel("Czas generowania hasha (sekundy)")
    ax2.set_title("Czas generowania hasha w zależności od długości danych")
    ax2.legend()
    ax2.grid()
    ax2.ticklabel_format(style='plain', axis='x')

    plt.tight_layout()
    plt.savefig("Wykresy.png", dpi=300)
    plt.show()

def find_collision(function, prefix_bits):
    seen = {}
    attempts = 0

    while True:
        attempts += 1
        text = ''.join(choice(ALPHABET) for _ in range(16))
        hash = generate_hash(text, function)

        bit_hash = bin(int(hash, 16))[2:].zfill(len(hash) * 4)
        prefix = bit_hash[:prefix_bits]

        if prefix in seen:
            return attempts, seen[prefix], text, prefix
        else:
            seen[prefix] = text

def bit_difference(hash1, hash2):
    bit_hash1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    bit_hash2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    return sum(bit1 != bit2 for bit1, bit2 in zip(bit_hash1, bit_hash2))

def flip_bit(text):
    bytes = bytearray(text, 'utf-8')

    byte_index = choice(range(len(bytes)))
    bit_index = choice(range(8))
    bytes[byte_index] ^= (1 << bit_index)

    return bytes.decode('utf-8', errors='ignore')

def avalanche_test(function, tests_num):
    results = []

    for _ in range(tests_num):
        text = ''.join(choice(ALPHABET) for _ in range(16))
        hash1 = generate_hash(text, function)

        modified_text = flip_bit(text)
        hash2 = generate_hash(modified_text, function)

        diff = bit_difference(hash1, hash2)
        results.append(diff / (len(hash1) * 4))

    avg = sum(results) / len(results)

    return avg

def main():
    #Podpunkt 2
    texts = ["a" * i for i in range(100000, 1000000, 100000)]
    compare_hashes(texts)

    #Podpunkt 3
    print(f"Wygenerowany hash dla słowa 'Owad': {generate_hash("Owad", "md5")}")
    #Po sprawdzeniu w wyszukiwarce, hash ten jest powszechnie znany

    #Podpunkt 4
    #MD5 nie jest funkcją bezpieczną, ponieważ znaleziono dla niej kolizje, pierwsze już w 2004 roku.
    #Dodatkowo MD5 jest bardzo szybka, co ułatwia ataki brute-force.

    # Podpunkt 5
    attempts, text1, text2, prefix = find_collision("sha3_512", 12)
    print(f"\nKolizja na pierwszych 12 bitach (SHA-3-512) znaleziona po {attempts} próbach:")
    print(f"Tekst 1: {text1}")
    print(f"Tekst 2: {text2}")
    print(f"Wspólne 12 bitów: {prefix}")
    print(f"Hash 1: {generate_hash(text1, "sha3_512")}")
    print(f"Hash 2: {generate_hash(text2, "sha3_512")}")

    # Podpunkt 6
    print("\nAvalanche test (SHA-3-512):")
    tests_num = 200
    print(f"Po {tests_num} próbach, średni procent zmienionych bitów po zmianie jednego bitu na wejściu: "
          f"{avalanche_test("sha3_512", tests_num)}")
    #Test się powiódł


main()