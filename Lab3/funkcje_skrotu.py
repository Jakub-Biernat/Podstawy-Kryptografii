import hashlib
import sys
import time
import matplotlib.pyplot as plt

def generate_and_compare_hashes(texts):
    functions = {
        'MD5': hashlib.md5(),
        'SHA1': hashlib.sha1(),
        'SHA2_224': hashlib.sha224(),
        'SHA2_256': hashlib.sha256(),
        'SHA2_384': hashlib.sha384(),
        'SHA2_512': hashlib.sha512(),
        'SHA3_224': hashlib.sha3_224(),
        'SHA3_256': hashlib.sha3_256(),
        'SHA3_384': hashlib.sha3_384(),
        'SHA3_512': hashlib.sha3_512(),
    }

    input_bits = []
    times = {name: [] for name in functions}
    hash_bits = {name: [] for name in functions}
    hashes = {}

    for text in texts:
        input_bits.append(len(text.encode()) * 8)
        for name, function in functions.items():
            start = time.perf_counter()
            function.update(text.encode())
            hash = function.hexdigest()
            stop = time.perf_counter()

            hashes[name] = hash
            times[name].append(stop - start)
            hash_bits[name].append(len(hash) * 4)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    for name in functions:
        plt.plot(input_bits, hash_bits[name], label=name)

    plt.xlabel("Długość danych wejściowych (bity)")
    plt.ylabel("Długość hasha (bity)")
    plt.title("Długość hasha od długości danych wejściowych")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    for name in functions:
        plt.plot(input_bits, times[name], label=name)
    plt.xlabel("Długość danych wejściowych (bity)")
    plt.ylabel("Czas wykonania (sekundy)")
    plt.title("Czas wykonania od długości danych wejściowych")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

def main():
    texts = [
        "a",
        "a" * 10,
        "a" * 100,
        "a" * 1000,
    ]

    generate_and_compare_hashes(texts)

main()