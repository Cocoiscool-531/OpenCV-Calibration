import cv2 as cv
import numpy as np
import glob
import time
from tqdm import tqdm

loaded = np.load("output/results.npz")
# print(results)
mtx = loaded['arr_0']
dist = loaded['arr_1']
camMatrix = loaded['arr_2']

startTime = time.time()

distorted = glob.glob('distorted/*.jpg')

for fname in tqdm(distorted, unit=" images", desc="Undistorting"):
    img = cv.imread(fname)
    h,  w = img.shape[:2]
    newCamMatrix, roi = cv.getOptimalNewCameraMatrix(camMatrix, dist, (w, h), 1, (w, h))

    # undistort
    # Test newcameramtx (calculated) vs camMatrix (found from 3d zephyr)
    dst = cv.undistort(img, mtx, dist, None, newCamMatrix)

    # crop the image
    # x, y, w, h = roi
    # dst = dst[y:y+h, x:x+w]

    path = "undistorted/" + (fname.split("/", 1)[1])

    cv.imwrite(path, dst)
print("Total runtime was {} seconds".format(time.time() - startTime))