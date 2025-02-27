import os

import datetime
import numpy as np
import cv2
import natsort

from GuidedFilter import GuidedFilter
from backgroundLight import BLEstimation
from depthMapEstimation import depthMap
from depthMin import minDepth
from getRGBTransmission import getRGBTransmissionESt
from global_Stretching import global_stretching
from refinedTransmissionMap import refinedtransmissionMap

from sceneRadiance import sceneRadianceRGB

np.seterr(over='ignore')
if __name__ == '__main__':
    pass

starttime = datetime.datetime.now()

folder = "E:/Code/Python/2023/Single-Underwater-Image-Enhancement-and-Color-Restoration/Datasets"

path = folder + "/Input"
files = os.listdir(path)
files =  natsort.natsorted(files)

for i in range(len(files)):
    file = files[i]
    filepath = path + "/" + file
    prefix = file.split('.')[0]
    if os.path.isfile(filepath):
        print('********    file   ********',file)
        img = cv2.imread(filepath)

        blockSize = 9
        gimfiltR = 50  # 引导滤波时半径的大小
        eps = 10 ** -3  # 引导滤波时epsilon的值

        DepthMap = depthMap(img)
        DepthMap = global_stretching(DepthMap)
        guided_filter = GuidedFilter(img, gimfiltR, eps)
        refineDR = guided_filter.filter(DepthMap)
        refineDR = np.clip(refineDR, 0,1)

        cv2.imwrite(folder+'/Output/ULAPDepthMap/'+file, np.uint8(refineDR * 255))

        AtomsphericLight = BLEstimation(img, DepthMap) * 255

        d_0 = minDepth(img, AtomsphericLight)
        d_f = 8 * (DepthMap + d_0)
        transmissionB, transmissionG, transmissionR = getRGBTransmissionESt(d_f)

        transmission = refinedtransmissionMap(transmissionB, transmissionG, transmissionR, img)
        sceneRadiance = sceneRadianceRGB(img, transmission, AtomsphericLight)


        cv2.imwrite(folder+'/Output/ULAP_TM/'+file, np.uint8(transmission[:, :, 2] * 255))


        # print('AtomsphericLight',AtomsphericLight)

        cv2.imwrite(folder+'/Output/ULAP/'+file, sceneRadiance)


Endtime = datetime.datetime.now()
Time = Endtime - starttime
print('Time', Time)


