import sys
import cv2
from secrets import choice
import numpy as np
from matplotlib import pyplot as plt


def split_image(image):
    h, w = image.shape[:2]
    share_image_1 = np.zeros((h * 2, w * 2), np.uint8)
    share_image_2 = np.zeros((h * 2, w * 2), np.uint8)

    white_pixel = [
        ([0, 0, 255, 255], [0, 0, 255, 255]),
        ([255, 255, 0, 0], [255, 255, 0, 0]),
        ([0, 255, 0, 255], [0, 255, 0, 255]),
        ([255, 0, 255, 0], [255, 0, 255, 0]),
    ]

    black_pixel = [
        ([255, 255, 0, 0], [0, 0, 255, 255]),
        ([0, 0, 255, 255], [255, 255, 0, 0]),
        ([0, 255, 0, 255], [255, 0, 255, 0]),
        ([255, 0, 255, 0], [0, 255, 0, 255]),
    ]

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if image[row][col] == 0:
                share_pixel_1, share_pixel_2 = choice(black_pixel)
            else:
                share_pixel_1, share_pixel_2 = choice(white_pixel)

            index = 0
            for row_offset in range(2):
                for col_offset in range(2):
                    share_image_1[row * 2 + row_offset, col * 2 + col_offset] = share_pixel_1[index]
                    share_image_2[row * 2 + row_offset, col * 2 + col_offset] = share_pixel_2[index]
                    index += 1

    return share_image_1, share_image_2

def join_images(share_image_1, share_image_2):
    return cv2.bitwise_and(share_image_1, share_image_2)

if __name__ == '__main__':
    #Wywołanie py ./visual_cryptography.py original_image_path
    original_image_path = sys.argv[1]
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)

    share_image_1, share_image2 = split_image(original_image)

    reconstructed_image = join_images(share_image_1, share_image2)

    titles = ['Oryginalny obrazek', 'Udzial 1', 'Udzial 2', 'Wynik zlozenia udzialow']
    images = [original_image, share_image_1, share_image2, reconstructed_image]

    plt.figure(figsize=(12, 8))

    for i in range(4):
        plt.subplot(2, 2, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()

