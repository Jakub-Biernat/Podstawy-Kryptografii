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

def compare_hashes(texts):
    functions = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']

    input_bits = []
    times = {name: [] for name in functions}
    hash_lengths = {name: [] for name in functions}

    for text in texts:
        input_bits.append(len(text_to_bits(text)))
        for function in functions:
            start = time.perf_counter()
            hash = generate_hash(text, function)
            stop = time.perf_counter()

            times[function].append(stop - start)
            hash_lengths[function].append(len(hash) * 4)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    for function in functions:
        plt.plot(input_bits, hash_lengths[function], label=function)

    plt.xlabel("Długość danych wejściowych (bity)")
    plt.ylabel("Długość wygenerowanego hasha (bity)")
    plt.title("Długość hasha w zależności od długości danych wejściowych")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    for function in functions:
        plt.plot(input_bits, times[function], label=function)
    plt.xlabel("Długość danych wejściowych (bity)")
    plt.ylabel("Czas generowania hasha (sekundy)")
    plt.title("Czas generowania hasha w zależności od długości danych wejściowych")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

def main():
    #Podpunkt 2
    texts = ["a" * i for i in range(100000, 1000000, 100000)]
    compare_hashes(texts)

    #Podpunkt 3
    print("Wygenerowany hash dla słowa 'Owad': " + generate_hash("Owad", "md5"))
    #Po sprawdzeniu w wyszukiwarce, hash ten jest powszechnie znany



main()