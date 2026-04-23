import hashlib
import time
import matplotlib.pyplot as plt


def generate_hash(text, function):
    hash = hashlib.new(function)
    hash.update(text.encode())
    return hash.hexdigest()

def text_to_bits(text, encoding='utf-8'):
    bytes_data = text.encode(encoding)
    bits = ''.join(format(byte, '08b') for byte in bytes_data)
    return bits

def generate_and_compare_hashes(texts):
    functions = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']

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
    print(generate_hash("Kot", 'sha1'))

main()