import os
import cv2 as cv
import numpy as np
import glob
import time
from tqdm import tqdm

UNDISTORT_CALIBRATION = False # If true, also undistorts all files in the calibration directory
FAST_RUN = False # Only fixes the first found image.

loaded = np.load("output/results.npz")
mtx = loaded['arr_0']
dist = loaded['arr_1']
camMatrix = loaded['arr_2']

startTime = time.time()

if input("Delete all files in undistorted directory? (y/N): ") == "y":
    undistorted = glob.glob("undistorted/*")
    for f in tqdm(undistorted, unit=" files", desc="Deleting"):
        os.remove(f)


distorted = glob.glob('distorted/*.jpg')
if UNDISTORT_CALIBRATION:
    distorted.extend(glob.glob('calibration/*.jpg'))

if FAST_RUN:
    distorted = [distorted[0]]

for fname in tqdm(distorted, unit=" images", desc="Undistorting"):
    img = cv.imread(fname)
    h,  w = img.shape[:2]
    # Test mtx (calculated) vs camMatrix (found from 3d zephyr)
    newCamMatrix, roi = cv.getOptimalNewCameraMatrix(camMatrix, dist, (w, h), 1, (w, h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newCamMatrix)

    # crop the image
    # x, y, w, h = roi
    # dst = dst[y:y+h, x:x+w]

    path = "undistorted/" + (fname.split("/", 1)[1])

    cv.imwrite(path, dst)
print("\nDone undistorting! Finished in {}s for {} images. Avg {}ms / image".format((time.time() - startTime), len(distorted), (1000*(time.time() - startTime))/len(distorted)))