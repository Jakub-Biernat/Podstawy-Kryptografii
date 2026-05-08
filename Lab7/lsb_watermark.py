import sys
import cv2
import matplotlib.pyplot as plt

def add_code_to_message(message):
    return "$$$" + message + "###"

def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)

def bits_to_text(bits):
    chars = []

    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))

    return ''.join(chars)

def extract_last_bits(image):
    h, w = image.shape[:2]
    total_bits = h * w * 3

    bits = []

    for idx in range(total_bits):
        pixel_index = idx // 3
        channel = idx % 3

        y = pixel_index // w
        x = pixel_index % w

        bit = image[y, x, channel] & 1
        bits.append(str(bit))

    return ''.join(bits)

def extract_message(text):
    start = "$$$"
    end = "###"

    s = text.find(start)
    e = text.find(end, s + len(start))

    if s == -1 or e == -1:
        return "BRAK"

    return text[s + len(start):e]

def lsb_watermark(image, message):
    h, w = image.shape[:2]
    watermark_image = image.copy()

    total_channels = h * w * 3

    message = add_code_to_message(message)
    message_bits = text_to_bits(message)
    n_message_bits = len(message_bits)

    if n_message_bits > total_channels:
        raise ValueError("Wiadomosc jest za dluga dla tych wymiarow obrazu")

    for i in range(n_message_bits):
        pixel_index = i // 3
        channel = i % 3

        y = pixel_index // w
        x = pixel_index % w

        watermark_image[y, x, channel] = (watermark_image[y, x, channel] & 254) | int(message_bits[i])

    return watermark_image

def decode_watermark_image(image):
    bits = extract_last_bits(image)
    text = bits_to_text(bits)
    message = extract_message(text)
    return message

def show_results(image, text, watermark_image, watermark_text):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"Oryginalny obraz\nWiadomość: {text}")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(watermark_image, cv2.COLOR_BGR2RGB))
    plt.title(f"Obraz ze znakiem wodnym\nWiadomość: {watermark_text}")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

def main():
    image = cv2.imread(sys.argv[1])
    message = sys.argv[2]

    text = decode_watermark_image(image)
    watermark_image = lsb_watermark(image, message)
    watermark_text = decode_watermark_image(watermark_image)

    show_results(image, text, watermark_image, watermark_text)

    #Czy taki sposób ukrywania informacji w obrazie jest odporny na ataki i próby
    #zniszczenia osadzonej wiadomości.
    #Nie, algorytm jest prosty a wiadomość ukryta jest w postaci jawnej. Ponadto algorytm
    #jest całkowicie nieodporny na modyfikacje obrazu takie jak kompresja czy zmiana rozmiaru.

    #Zaproponuj ataki na osadzoną wiadomość
    #Kompresja jpeg
    #Zmiana rozdzielczości
    #Analiza statystyczna
    #Atak nadpisania

    #Jaki jest rozmiar wiadomości możliwej do ukrycia?
    #Liczba pikseli x 3 (w bitach)

main()