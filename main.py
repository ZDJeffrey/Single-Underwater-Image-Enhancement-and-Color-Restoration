import os
import numpy as np
import cv2
import natsort
import matplotlib.pyplot as plt
from uqim_utils import getUIQM
from Retinex import *
from CLAHE import *

def gamma_correction(image, gamma=1.0):
    # 构建伽马矫正查找表
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    # 应用查找表
    corrected_image = cv2.LUT(image, table)
    return corrected_image

import argparse

if __name__ == "__main__":
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description='Process some algorithms to recover underwater images.')

    # 添加命令行参数
    parser.add_argument('algorithm', choices=['CLAHE', 'CLAHE_mix','MSRCR','MSRCR_CLAHE'], help='Specify the algorithm (CLAHE, CLAHE_mix, MSRCR, MSRCR_CLAHE)')

    # 解析命令行参数
    args = parser.parse_args()

    np.seterr(over='ignore')
    plt.figure(figsize=(16, 9))
    folder = "E:/Code/Python/2023/Single-Underwater-Image-Enhancement-and-Color-Restoration/Datasets"
    input_path = folder + "/Input"
    output_path = folder + "/Output"
    files = os.listdir(input_path)
    files =  natsort.natsorted(files)

    sumuiqm_origin  = 0.
    sumuiqm_recover  = 0.

    cols = len(files)

    for i in range(len(files)):
        file = files[i]
        filepath = input_path + "/" + file
        if os.path.isfile(filepath):
            img = cv2.imread(filepath)
            
            if args.algorithm == 'CLAHE':
                img_recover = CLAHE(img,1.0,(4,4))
            elif args.algorithm == 'CLAHE_mix':
                img_recover = mix_CLAHE(img,1.0,(4,4))
            elif args.algorithm == 'MSRCR':
                img_recover = MSRCR(img)
            elif args.algorithm == 'MSRCR_CLAHE':
                img_recover = CLAHE(MSRCR(img),1.0,(4,4))
            else:
                print("Error: algorithm not found!")
                break

            cv2.imwrite(output_path + "/" + args.algorithm + "_" + file, img_recover)

            uiqm_origin = getUIQM(img)
            uiqm_recover = getUIQM(img_recover)

            sumuiqm_origin += uiqm_origin
            sumuiqm_recover += uiqm_recover

            plt.subplot(2, cols, i + 1)
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.title(f"UIQM: {uiqm_origin:.3f}")
            plt.axis('off')

            plt.subplot(2, cols, i + 1 + cols)
            plt.imshow(cv2.cvtColor(img_recover, cv2.COLOR_BGR2RGB))
            plt.title(f"UIQM: {uiqm_recover:.3f}")
            plt.axis('off')

    print(f"Average UIQM of origin images: {sumuiqm_origin / len(files):.3f}")
    print(f"Average UIQM of recover images: {sumuiqm_recover / len(files):.3f}")

    plt.tight_layout()
    plt.show()

