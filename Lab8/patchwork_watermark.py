import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

DELTA = 1.0

def create_rng(key):
    return np.random.default_rng(key)


def select_pairs(rng, n, image):
    h, w = image.shape[:2]
    for _ in range(n):
        a = (rng.integers(0, h), rng.integers(0, w))
        b = (rng.integers(0, h), rng.integers(0, w))
        yield a, b

def watermark(image, key, n):
    img = image.astype(np.float32).copy()
    rng = create_rng(key)

    for (ax, ay), (bx, by) in select_pairs(rng, n, img):
        img[ax, ay] += DELTA
        img[bx, by] -= DELTA

    return np.clip(img, 0, 255).astype(np.uint8)

def detect(image, key, n):
    img = image.astype(np.float32)
    rng = create_rng(key)

    S = 0.0

    for (ax, ay), (bx, by) in select_pairs(rng, n, img.shape):
        S += img[ax, ay] - img[bx, by]

    if S > 0:
        return "Znak wodny wykryty"
    else:
        return "Znak wodny niewykryty"

def show_results(original_image, watermark_image, key, n):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(original_image, cmap="gray")
    axs[0].set_title("Oryginalny obrazek")
    axs[0].axis("off")

    axs[1].imshow(watermark_image, cmap="gray")
    axs[1].set_title(f"Obraz ze znakiem wodnym\nDetekcja: {detect(watermark_image, key, n)}")
    axs[1].axis("off")

    plt.tight_layout()
    plt.show()

def main():
    #Uruchomienie: py .\patchwork_watermark.py obraz klucz n
    image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    key = int(sys.argv[2])
    n = int(sys.argv[3])

    watermark_image = watermark(image, key, n)
    cv2.imwrite("obraz_znak_wodny.png", watermark_image)

main()