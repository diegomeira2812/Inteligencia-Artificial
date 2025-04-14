# pip install opencv-python

import math
import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('./imagens/girafa.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
a = img_gray.max()
_, thresh = cv2.threshold(img_gray, a / 2 * 1.7, a, cv2.THRESH_BINARY_INV)

tamanhoKernel = 5
kernel = np.ones((tamanhoKernel, tamanhoKernel), np.uint8)
thresh_open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

img_blur = cv2.blur(img_gray, ksize=(tamanhoKernel, tamanhoKernel))

edges_gray = cv2.Canny(image=img_gray, threshold1=a/2, threshold2=a/2)
edges_blur = cv2.Canny(image=img_blur, threshold1=a/2, threshold2=a/2)

contours, hierarchy = cv2.findContours(
    image=thresh_open,
    mode=cv2.RETR_TREE,
    method=cv2.CHAIN_APPROX_SIMPLE
)

contours = sorted(contours, key=cv2.contourArea, reverse=True)
contours = [c for c in contours if cv2.contourArea(c) > 500]

img_copy = img.copy()
final = cv2.drawContours(img_copy, contours, contourIdx=-1, color=(255, 0, 0), thickness=2)

imagens = [img, img_gray, img_blur, edges_gray, edges_blur, thresh, thresh_open, final]
titulos = ['Original (RGB)', 'Cinza', 'Blur', 'Canny Gray', 'Canny Blur', 'Threshold', 'Open', 'Contornos']

formatoX = math.ceil(len(imagens) ** 0.5)
formatoY = formatoX if (formatoX**2 - len(imagens)) <= formatoX else formatoX - 1

plt.figure(figsize=(15, 10))
for i in range(len(imagens)):
    plt.subplot(formatoY, formatoX, i + 1)
    if len(imagens[i].shape) == 2:
        plt.imshow(imagens[i], cmap='gray')
    else:
        plt.imshow(imagens[i])
    plt.title(titulos[i], fontsize=10)
    plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.show()
