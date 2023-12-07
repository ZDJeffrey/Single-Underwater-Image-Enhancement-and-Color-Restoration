import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取RGB图像
image_path = "Datasets/Input/3.jpg"
# image_path = "Datasets/Input/16.jpg"
# image_path = "Datasets/Input/47.jpg"
# image_path = "Datasets/Input/246.jpg"
# image_path = "Datasets/Input/554.jpg"
# image_path = "Datasets/Input/2129.jpg"
# image_path = "Datasets/Input/2552.jpg"
# image_path = "Datasets/Input/5015.jpg"

image = cv2.imread(image_path)

# 检查图像是否成功加载
if image is None:
    print("无法加载图像")
else:
    # 分离通道
    b, g, r = cv2.split(image)

    # 显示原始图像和分离的通道
    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")

    plt.subplot(2, 2, 2)
    plt.imshow(b, cmap='gray')
    plt.title("Blue Channel")

    plt.subplot(2, 2, 3)
    plt.imshow(g, cmap='gray')
    plt.title("Green Channel")

    plt.subplot(2, 2, 4)
    plt.imshow(r, cmap='gray')
    plt.title("Red Channel")
    plt.show()
