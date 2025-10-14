import numpy as np
import cv2 as cv
import glob

width = 5
height = 8

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((width*height,3), np.float32)
objp[:,:2] = np.mgrid[0:width,0:height].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('distorted/images/*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #cv.imwrite("gray.jpg", gray)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (width,height), None)
    print(ret, corners)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        # cv.drawChessboardCorners(img, (width,height), corners2, ret)
        #cv.imwrite("corners.jpg", img)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None, flags=cv.CALIB_RATIONAL_MODEL)
dist1, rvecs1, tvecs1 = None, None, None
cv.fisheye.calibrate(objpoints, imgpoints, gray.shape[::-1], mtx, dist1, rvecs1, tvecs1)

for fname in glob.glob("distorted/images/*.jpg"):
    img = cv.imread(fname)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    dst1 = None
    cv.fisheye.undistortImage(img, mtx, dist, dst1, None, (w, h))

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite("undistorted/" + fname, dst)
    cv.imshow("Distorted", img)
    cv.waitKey(500)
    cv.destroyAllWindows()
    cv.imshow("Undistorted", dst)
    cv.waitKey(500)