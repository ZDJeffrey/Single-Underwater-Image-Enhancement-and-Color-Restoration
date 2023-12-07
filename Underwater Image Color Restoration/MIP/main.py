import os
import numpy as np
import cv2
import natsort

from BL import getAtomsphericLight
from EstimateDepth import DepthMap
from getRefinedTramsmission import Refinedtransmission
from TM import getTransmission
from sceneRadiance import sceneRadianceRGB

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

        blockSize = 9

        largestDiff = DepthMap(img, blockSize)
        transmission = getTransmission(largestDiff)
        transmission = Refinedtransmission(transmission,img)
        AtomsphericLight = getAtomsphericLight(transmission, img)
        sceneRadiance = sceneRadianceRGB(img, transmission, AtomsphericLight)

        cv2.imwrite(folder+'/Output/MIP_TM/'+file, np.uint8(transmission * 255))
        cv2.imwrite(folder+'/Output/MIP/'+file, sceneRadiance)
