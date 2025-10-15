import numpy as np
import cv2 as cv
import glob
from tqdm import tqdm

width = 5
height = 8

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((width*height,3), np.float32)
objp[:,:2] = np.mgrid[0:width,0:height].T.reshape(-1,2)

fx = 595.21
fy = 595.21
cx = 984.515
cy = 599.035

# Arrays to store object points and image points from all the images.
objPoints = [] # 3d point in real world space
imgPoints = [] # 2d points in image plane.

#  ---       ---
# | fx   0   cx |
# | 0   fy   cy |
# | 0    0    1 |
#  ---       ---
camMatrix = np.array([np.array([fx, 0, cx]), np.array([0, fy, cy]), np.array([0, 0, 1])])

images = glob.glob('calibration/*.jpg')
i = 0

for fname in tqdm(images, unit=" images", desc="Gathering data"):
    i += 1
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #cv.imwrite("gray.jpg", gray)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (width,height), None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        objPoints.append(objp)

        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners2)

        # Draw and display the corners
        # cv.drawChessboardCorners(img, (width,height), corners2, ret)
        #cv.imwrite("corners.jpg", img)

cv.destroyAllWindows()

print("Calibrating matrices:")
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None, flags=cv.CALIB_RATIONAL_MODEL)

file = "results.npz"
np.savez(file, mtx, dist, camMatrix)
print("Results saved to '{}'!".format(file))