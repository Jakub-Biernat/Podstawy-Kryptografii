from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time
import matplotlib.pyplot as plt

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

def generate_ciphertext(cipher, mode, text):
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
    modes = {
        "ECB": AES.MODE_ECB,
        "CBC": AES.MODE_CBC,
        "CFB": AES.MODE_CFB,
        "OFB": AES.MODE_OFB,
        "CTR": AES.MODE_CTR
    }

    key = get_random_bytes(16)
    input_bits = []
    enc_times = {name: [] for name in modes.keys()}
    dec_times = {name: [] for name in modes.keys()}

    for text in texts:
        text = add_padding(text)
        input_bits.append(len(text))
        for mode_name, mode in modes.items():
            cipher = generate_cipher(mode, key)
            start_enc = time.perf_counter()
            ciphertext = generate_ciphertext(cipher, mode, text)
            stop_enc = time.perf_counter()
            enc_times[mode_name].append(stop_enc - start_enc)

            decipher = generate_decipher(mode, key, cipher)
            start_dec = time.perf_counter()
            decrypted = generate_decrypted(decipher, ciphertext)
            stop_dec = time.perf_counter()
            dec_times[mode_name].append(stop_dec - start_dec)

    plt.figure(figsize=(12, 6))

    ax1 = plt.subplot(1, 2, 1)
    for mode in modes.keys():
        ax1.plot(input_bits, enc_times[mode], label=mode)

    ax1.set_xlabel("Długość danych wejściowych (bity)")
    ax1.set_ylabel("Czas szyfrowania (sekundy)")
    ax1.set_title("Czas szyfrowania AES w zależności od długości danych")
    ax1.legend()
    ax1.grid()
    ax1.ticklabel_format(style='plain', axis='x')

    ax2 = plt.subplot(1, 2, 2)
    for mode in modes.keys():
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

def main():
    #Podpunkt 1
    texts = ["a" * i for i in range(100000, 1000000, 100000)]
    compare_modes(texts)

main()