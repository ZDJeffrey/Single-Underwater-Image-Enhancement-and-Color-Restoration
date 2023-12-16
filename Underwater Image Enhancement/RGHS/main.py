import os
import numpy as np
import cv2
import natsort

from LabStretching import LABStretching
from global_stretching_RGB import stretching

np.seterr(over='ignore')
if __name__ == '__main__':
    pass

folder = "E:/Code/Python/2023/Single-Underwater-Image-Enhancement-and-Color-Restoration/Datasets"

path = folder + "/Input"
files = os.listdir(path)
files =  natsort.natsorted(files)

for i in range(len(files)):
    file = files[i]
    filepath = path + "/" + file
    if os.path.isfile(filepath):
        print('********    file   ********',file)
        img = cv2.imread(filepath)
        height = len(img)
        width = len(img[0])
        sceneRadiance = img
        sceneRadiance = stretching(sceneRadiance)
        sceneRadiance = LABStretching(sceneRadiance)
        cv2.imwrite(folder+'/Output/RGHS/' + file, sceneRadiance)
