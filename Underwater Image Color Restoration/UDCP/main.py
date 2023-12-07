import os
import numpy as np
import cv2
import natsort

from RefinedTramsmission import Refinedtransmission
from getAtomsphericLight import getAtomsphericLight
from getGbDarkChannel import getDarkChannel
from getTM import getTransmission
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

        print('img',img)

        blockSize = 9
        GB_Darkchannel = getDarkChannel(img, blockSize)
        AtomsphericLight = getAtomsphericLight(GB_Darkchannel, img)

        print('AtomsphericLight', AtomsphericLight)
        # print('img/AtomsphericLight', img/AtomsphericLight)

        # AtomsphericLight = [231, 171, 60]

        transmission = getTransmission(img, AtomsphericLight, blockSize)

        # cv2.imwrite('OutputImages/' + prefix + '_UDCP_Map.jpg', np.uint8(transmission))

        transmission = Refinedtransmission(transmission, img)
        sceneRadiance = sceneRadianceRGB(img, transmission, AtomsphericLight)
        # print('AtomsphericLight',AtomsphericLight)

        cv2.imwrite(folder+'/Output/UDCP_TM/'+file, np.uint8(transmission* 255))
        cv2.imwrite(folder+'/Output/UDCP/'+file, sceneRadiance)


