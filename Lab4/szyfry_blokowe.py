from secrets import choice
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time
import matplotlib.pyplot as plt

MODES = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "CFB": AES.MODE_CFB,
    "OFB": AES.MODE_OFB,
    "CTR": AES.MODE_CTR
}

def add_padding(text):
    text = text.encode()
    return text + b' ' * (16 - len(text) % 16)

def generate_cipher(mode, key):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    elif mode == AES.MODE_CTR:
        return AES.new(key, mode, nonce=get_random_bytes(8))
    else:
        iv = get_random_bytes(16)
        cipher = AES.new(key, mode, iv=iv)

    return cipher

def generate_ciphertext(cipher, text):
    return cipher.encrypt(text)

def generate_decipher(mode, key, cipher):
    if mode == AES.MODE_ECB:
        decipher = AES.new(key, mode)
    elif mode == AES.MODE_CTR:
        decipher = AES.new(key, mode, nonce=cipher.nonce)
    else:
        decipher = AES.new(key, mode, iv=cipher.iv)

    return decipher

def generate_decrypted(decipher, ciphertext):
    return decipher.decrypt(ciphertext)

def compare_modes(texts):
    key = get_random_bytes(16)
    input_bits = []
    enc_times = {name: [] for name in MODES.keys()}
    dec_times = {name: [] for name in MODES.keys()}

    for text in texts:
        text = add_padding(text)
        input_bits.append(len(text) * 8)
        for mode_name, mode in MODES.items():
            cipher = generate_cipher(mode, key)
            start_enc = time.perf_counter()
            ciphertext = generate_ciphertext(cipher, text)
            stop_enc = time.perf_counter()
            enc_times[mode_name].append(stop_enc - start_enc)

            decipher = generate_decipher(mode, key, cipher)
            start_dec = time.perf_counter()
            decrypted = generate_decrypted(decipher, ciphertext)
            stop_dec = time.perf_counter()
            dec_times[mode_name].append(stop_dec - start_dec)

    plt.figure(figsize=(12, 6))

    ax1 = plt.subplot(1, 2, 1)
    for mode in MODES.keys():
        ax1.plot(input_bits, enc_times[mode], label=mode)

    ax1.set_xlabel("Długość danych wejściowych (bity)")
    ax1.set_ylabel("Czas szyfrowania (sekundy)")
    ax1.set_title("Czas szyfrowania AES w zależności od długości danych")
    ax1.legend()
    ax1.grid()
    ax1.ticklabel_format(style='plain', axis='x')

    ax2 = plt.subplot(1, 2, 2)
    for mode in MODES.keys():
        ax2.plot(input_bits, dec_times[mode], label=mode)

    ax2.set_xlabel("Długość danych wejściowych (bity)")
    ax2.set_ylabel("Czas deszyfrowania (sekundy)")
    ax2.set_title("Czas deszyfrowania AES w zależności od długości danych")
    ax2.legend()
    ax2.grid()
    ax2.ticklabel_format(style='plain', axis='x')

    plt.tight_layout()
    plt.savefig("Wykresy.png", dpi=300)
    plt.show()

    return

def flip_bit(text):
    byte_arr = bytearray(text)
    byte_index = choice(range(len(byte_arr)))
    bit_index = choice(range(8))
    byte_arr[byte_index] ^= (1 << bit_index)
    return bytes(byte_arr)

def byte_difference(originaltext, decrypted):
    length = min(len(originaltext), len(decrypted))
    return sum(1 for i in range(length) if originaltext[i] != decrypted[i])

def test_modes_error_propagation():
    text = "Litwo! Ojczyzno moja! ty jestes jak zdrowie. Ile cie trzeba cenic, ten tylko sie dowie. Kto cie stracil."
    print("Test propagacji błędu")
    print(f"Oryginalny tekst: {text}")
    key = get_random_bytes(16)

    padded_text = add_padding(text)
    for mode_name, mode in MODES.items():
        cipher = generate_cipher(mode, key)
        ciphertext = generate_ciphertext(cipher, padded_text)

        corrupted = flip_bit(ciphertext)

        decipher = generate_decipher(mode, key, cipher)
        decrypted = generate_decrypted(decipher, corrupted)

        byte_diff = byte_difference(padded_text, decrypted)
        decrypted = decrypted.decode('utf-8', errors='ignore')
        print(f"Propagacja błędu {mode_name}")
        print(f"Odszyfrowany tekst: {decrypted}")
        if byte_diff == 1:
            print(f"{mode_name}: 1 bajt został zmieniony, brak propagacji na inne bajty")
        elif byte_diff <= 16:
            print(f"{mode_name}: 1 blok uszkodzony, zmianie uległo {byte_diff} bajtów")
        else:
            print(f"{mode_name}: Propagacja błędu, zmianie uległo {byte_diff} bajtów")

def main():
    #Podpunkt 1
    texts = ["a" * i for i in range(100000, 1000000, 100000)]
    compare_modes(texts)

    #Podpunkt 2
    test_modes_error_propagation()

main()