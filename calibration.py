import numpy as np
import cv2 as cv
import glob
from tqdm import tqdm
import xml.etree.cElementTree as ET
from xml.dom.minidom import parseString
import time

patternWidth = 5
patternHeight = 8
resolutionWidth = 1920
resolutionHeight = 1200
cameraName = "ELP High Speed Global Shutter 120degree"
cameraVid = "0x32E4"
cameraPid = "0x0234"

fx = 595.21
fy = 595.21
cx = 984.515
cy = 599.035

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((patternWidth * patternHeight, 3), np.float32)
objp[:,:2] = np.mgrid[0:patternWidth, 0:patternHeight].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objPoints = [] # 3d point in real world space
imgPoints = [] # 2d points in image plane.

#  ---       ---
# | fx   0   cx |
# | 0   fy   cy |
# | 0    0    1 |
#  ---       ---

camMatrix = np.array([np.array([fx, 0, cx]), np.array([0, fy, cy]), np.array([0, 0, 1])])

i = 0
timer = time.time()
images = glob.glob('calibration/*.jpg')
for fileName in tqdm(images, unit=" images", desc="Gathering data"):
    i += 1
    img = cv.imread(fileName)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (patternWidth, patternHeight), None)

    # If found, add object points, image points (after refining them)
    if ret:

        objPoints.append(objp)

        corners = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners)

print("\nDone gathering data! Finished in {}s for {} images. Avg {}ms / image".format((time.time() - timer), len(images), (1000*(time.time() - timer))/len(images)))

print("\nCalibrating matrices:")

timer = time.time_ns()
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None, flags=cv.CALIB_RATIONAL_MODEL)
print("\nDone calibrating! Finished in {}ms".format((time.time_ns() - timer)/1000000))

file = "results.npz"
np.savez(file, mtx, dist, camMatrix)
print("\nnpz results saved to '{}'!".format(file))
print("\nSaving to xml:")

# Create XML file using camMatrix and distortion coefficients
coefficients = dist[0]

coefficientsAsString = (str(coefficients[0]) + "f, " +
                        str(coefficients[1]) + "f, " +
                        str(coefficients[2]) + "f, " +
                        str(coefficients[3]) + "f, " +
                        str(coefficients[4]) + "f, " +
                        str(coefficients[5]) + "f, " +
                        str(coefficients[6]) + "f")

root = ET.Element("Calibrations")

camera = ET.SubElement(root, "Camera", vid=cameraVid, pid=cameraPid)

camera.insert(1, ET.Comment(cameraName + " - Calibrated using OpenCV tooling - Script created by Team 19410. Calibrated to 8 distortion coefficients "))


calibration = ET.SubElement(camera, "Calibration",
                            size                   = str(resolutionWidth) + " " + str(resolutionHeight),
                            focalLength            = str(fx) + "f, " + str(fy) + "f",
                            principalPoint         = str(cx) + "f, " + str(cy) + "f",
                            distortionCoefficients = coefficientsAsString)

xmlString = parseString(ET.tostring(root, 'utf-8', xml_declaration=False)).toprettyxml(indent=" ").replace("<?xml version=\"1.0\" ?>", "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>")

with open("calibrated.xml", "w") as file:
    file.writelines(xmlString)



