import hashlib
import sys
import time


def generate_and_compare_hashes(text):
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

    input_bits = len(text.encode()) * 8
    print("########################################################## TEST DANYCH WEJSCIOWYCH DLUGOSCI " +
          str(input_bits) + " BITOW ##########################################################")

    hashes = {}
    for name, function in functions.items():
        start = time.time()
        function.update(text.encode())
        hash = function.hexdigest()
        stop = time.time()
        hashes[name] = hash
        output_bits = len(hash) * 4
        print("Wygenerowany hash przy uzyciu algorytmu " + name + ": " + hashes[name])
        print("Czas dzialania tego algorytmu: " + str(stop - start) + "sekund")
        print("Dlugosc ciagu wyjsciowego: " + str(output_bits) + " bitow")
        print()

def main():
    textfile = sys.argv[1]
    with open(textfile, 'r') as f:
        text = f.read()
        generate_and_compare_hashes(text)

main()