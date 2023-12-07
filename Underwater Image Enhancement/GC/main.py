
import os
import numpy as np
import cv2
import natsort
from skimage import exposure

from sceneRadianceGC import RecoverGC

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
        sceneRadiance = RecoverGC(img)
        print('sceneRadiance',sceneRadiance)
        cv2.imwrite(folder+'/Output/GC/'+file, sceneRadiance)
