import os
import numpy as np
import cv2
import natsort

def RecoverCLAHE(img):
    clahe = cv2.createCLAHE(clipLimit=4, tileGridSize=(2, 2))
    recover_img=img.copy()
    recover_img[:, :] = clahe.apply((img[:, :]))
    return recover_img

np.seterr(over='ignore')
if __name__ == '__main__':
    folder = "E:/Code/Python/2023/Single-Underwater-Image-Enhancement-and-Color-Restoration/Datasets"
    path = folder + "/Input"
    files = os.listdir(path)
    files =  natsort.natsorted(files)

    for i in range(len(files)):
        file = files[i]
        filepath = path + "/" + file
        if os.path.isfile(filepath):
            img = cv2.imread(filepath)
            recover_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            recover_rgb = img.copy()
            for i in range(3):
                recover_rgb[:,:,i] = RecoverCLAHE(recover_rgb[:,:,i])

            for i in range(1,3):
                recover_hsv[:,:,i] = RecoverCLAHE(recover_hsv[:,:,i])
    
            cv2.imshow('img',img)
            cv2.imshow('recover_hsv',cv2.cvtColor(recover_hsv,cv2.COLOR_HSV2BGR))
            cv2.imshow('recover_rgb',recover_rgb)
            cv2.waitKey(-1)
    cv2.destroyAllWindows()
