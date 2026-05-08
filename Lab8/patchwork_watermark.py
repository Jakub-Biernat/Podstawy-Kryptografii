import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

DELTA = 5.0
THRESHOLD = 10

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

    s = 0.0
    for (ax, ay), (bx, by) in select_pairs(rng, n, img):
        s += img[ax, ay]
        s += img[bx, by]
        img[ax, ay] += DELTA
        img[bx, by] -= DELTA

    return np.clip(img, 0, 255).astype(np.uint8), s

def detect(image, key, n, s):
    img = image.astype(np.float32).copy()
    rng = create_rng(key)
    s_prim = 0.0

    for (ax, ay), (bx, by) in select_pairs(rng, n, img):
        img[ax, ay] -= DELTA
        img[bx, by] += DELTA
        s_prim += img[ax, ay]
        s_prim += img[bx, by]

    if abs(s_prim - s) > THRESHOLD:
        return "Znak wodny niewykryty"
    else:
        return "Znak wodny wykryty"

def noise_image(image):
    noise = np.random.normal(0, 2, image.shape)
    noised = image.astype(np.float32) + noise
    return np.clip(noised, 0, 255).astype(np.uint8)

def show_results(original_image, watermark_image, modified_watermark_image, key, n, s):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].imshow(original_image, cmap="gray")
    axs[0].set_title("Oryginalny obrazek")
    axs[0].axis("off")

    axs[1].imshow(watermark_image, cmap="gray")
    axs[1].set_title("Obrazek ze znakiem wodnym\nDetekcja: " + detect(watermark_image, key, n, s))
    axs[1].axis("off")

    axs[2].imshow(modified_watermark_image, cmap="gray")
    axs[2].set_title("Zmodyfikowany obrazek ze znakiem wodnym\nDetekcja: " + detect(modified_watermark_image, key, n, s))
    axs[2].axis("off")

    plt.tight_layout()
    plt.show()

def main():
    #Uruchomienie: py .\patchwork_watermark.py obraz klucz n
    image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    key = int(sys.argv[2])
    n = int(sys.argv[3])

    watermark_image, s = watermark(image, key, n)
    cv2.imwrite("obraz_znak_wodny.png", watermark_image)

    modified_watermark_image = noise_image(watermark_image)
    cv2.imwrite("zmodyfikowany_obraz_znak_wodny.png", modified_watermark_image)

    show_results(image, watermark_image, modified_watermark_image, key, n, s)

main()