import numpy as np
import cv2

def CLAHE(img,clipLimit=2.0,tileGridSize=(4,4)):
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    recover_img=img.copy()
    for i in range(img.shape[2]):
        recover_img[:, :,i] = clahe.apply((img[:, :,i]))
    return recover_img

def mix_CLAHE(img,clipLimit=2.0,tileGridSize=(4,4)):
    img1 = img.copy()
    img1 = CLAHE(img1,clipLimit,tileGridSize)
    img1 = img1.astype(np.float32) / 255.0
    img1 = img1 / np.sum(img1, axis=2, keepdims=True)
    img1 = img1**2
    
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img2[:,:,1:] = CLAHE(img2[:,:,1:],clipLimit,tileGridSize)
    img2 = cv2.cvtColor(img2, cv2.COLOR_HSV2BGR)
    img2 = img2.astype(np.float32) / 255.0
    img2 = img2**2

    mix = (img1 + img2)**0.5
    mix = np.clip(mix, 0, 1)
    mix = (mix * 255).astype(np.uint8)
    return mix


# 读取图像
image = cv2.imread('E:/Code/Python/2023/Single-Underwater-Image-Enhancement-and-Color-Restoration/Datasets/Input/3.jpg')

# 进行直方图均衡
for i in range(3):
    image[:, :, i] = cv2.equalizeHist(image[:, :, i])

cv2.imshow('image', image)
cv2.waitKey(0)