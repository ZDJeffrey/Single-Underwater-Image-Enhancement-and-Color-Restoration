import numpy as np
import cv2
from CLAHE import CLAHE


def simplestColorBalance(img, low_clip, high_clip):
    total = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):            
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c  
        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)
    return img

def MSRCR(img, sigma_list=[15,81,250], alpha=125.0, beta=46.0):
    img_float = np.float64(img)/255.0+1.0
    retinex = np.zeros_like(img_float)
    for sigma in sigma_list:
        retinex += np.log10(img_float) - np.log10(cv2.GaussianBlur(img_float, (0, 0), sigma))
    img_retinex = retinex / len(sigma_list)
    img_sum = np.sum(img_float, axis=2, keepdims=True)
    img_color = np.log10(alpha * img_float / img_sum)
    img_msrcr = beta * img_retinex * img_color
    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255
    msrcr = np.clip(img_msrcr, 0, 255).astype(np.uint8)
    msrcr = simplestColorBalance(msrcr, 0.01, 0.99)
    return msrcr

def MSRCR_CLAHE(img, sigma_list=[15,81,250], alpha=125.0, beta=46.0):
    img_float = np.float64(img)/255.0+1.0
    retinex = np.zeros_like(img_float)
    for sigma in sigma_list:
        retinex += np.log10(img_float) - np.log10(cv2.GaussianBlur(img_float, (0, 0), sigma))
    img_retinex = retinex / len(sigma_list)
    img_sum = np.sum(img_float, axis=2, keepdims=True)
    img_color = np.log10(alpha * img_float / img_sum)
    img_msrcr = beta * img_retinex * img_color
    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255
    msrcr = np.clip(img_msrcr, 0, 255).astype(np.uint8)
    msrcr = CLAHE(msrcr,1.0,(4,4))
    return msrcr
