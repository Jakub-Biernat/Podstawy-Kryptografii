import hashlib
import sys


def generate_hash(text):
    functions = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha224': hashlib.sha224(),
        'sha256': hashlib.sha256(),
        'sha384': hashlib.sha384(),
        'sha512': hashlib.sha512(),
        'sha3_224': hashlib.sha3_224(),
        'sha3_256': hashlib.sha3_256(),
        'sha3_384': hashlib.sha3_384(),
        'sha3_512': hashlib.sha3_512(),
    }

    for name, function in functions.items():
        function.update(text.encode())
        print("Wygenerowany hash przy uzyciu algorytmu " + name + ":" + function.hexdigest())

def main():
    textfile = sys.argv[1]
    with open(textfile, 'r') as f:
        text = f.read()
        generate_hash(text)

main()