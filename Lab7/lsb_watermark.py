import sys
import cv2
from secrets import choice
import matplotlib.pyplot as plt



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

def lsb_watermark(image, message):
    h, w = image.shape[:2]
    watermark_image = image.copy()

    total_channels = h * w * 3

    message_bits = text_to_bits(message)
    n_message_bits = len(message_bits)

    if n_message_bits > total_channels:
        raise ValueError("Wiadomosc jest za dluga dla tych wymiarow obrazu")

    start_channel = choice(range(total_channels - n_message_bits + 1))

    for i in range(n_message_bits):
        idx = start_channel + i

        pixel_index = idx // 3
        channel = idx % 3

        y = pixel_index // w
        x = pixel_index % w

        watermark_image[y, x, channel] = (watermark_image[y, x, channel] & ~1) | int(message_bits[i])

    return watermark_image

def decode_watermark_image(image):
    bits = extract_last_bits(image)
    return bits_to_text(bits)


def main():
    image = cv2.imread(sys.argv[1])
    message = sys.argv[2]

    no_watermark_text = decode_watermark_image(image)
    watermark_image = lsb_watermark(image, message)
    watermark_text = decode_watermark_image(watermark_image)


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