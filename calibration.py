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

fx = 595.21
fy = 595.21
cx = 984.515
cy = 599.035

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
camMatrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])


images = glob.glob('images/*.jpg')
i = 0
for fname in images:
    i += 1
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #cv.imwrite("gray.jpg", gray)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (width,height), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print(i)
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        # cv.drawChessboardCorners(img, (width,height), corners2, ret)
        #cv.imwrite("corners.jpg", img)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None, flags=cv.CALIB_RATIONAL_MODEL)
with open("coefficients.txt", "w") as file:
    file.write(str(dist))

distorted = glob.glob('distorted/*.jpg')
for fname in distorted:
    img = cv.imread(fname)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    # x, y, w, h = roi
    # dst = dst[y:y+h, x:x+w]
    print("undistorted/" + str(fname))
    cv.imwrite("undistorted/" + str(fname), dst)
    cv.imshow("undistorted", dst)
    cv.waitKey(250)