# OpenCV-Calibration

Pretty easy
<br>Put .jpg files in calibration folder, put as many pictures of the same checkered pattern as you can in here. If needed.

<br>In calibration.py, fill in the values as follows:

```
patternWidth - Countable intersections on the checker pattern horizontally.
patternHeight - Countable intersections on the checker pattern vertically.
```
Note: This only counts intersections that can be identified by OpenCV, so if the corner is white, and the surrounding is white, so that you can't visually see the intersection, it doesn't count in the pattern count.
```
resolutionWidth - Width, in pixels, of the images.
resolutionHeight - Height, in pixels, of the images.
```
The following are used in the saved xml file. [You can find VID and PID here](https://www.nodeloop.org/projects/usb-identifer)
```
cameraName - Name of the camera - cosmetic
cameraVid - Vender ID of the camera - used by the FTC SDK to identify when to use the generated calibration file
cameraPid - Product ID of the camera - used by the FTC SDK to identify when to use the generated calibration file
```

Once these are set, you can run calibration.py. Depending on how many pictures you have, this may take a long time.

After it's finished, you should get a calibrated.xml and results.npz file in the output directory. If you're missing modules, run `pip3 install -r requirements.txt` to install all required modules.

If you'd like, you can put images in the distorted folder, and run undistort.py to use the calibrated values to undistort the images, the undistorted images will then be placed in the undistorted directory, with the same name as their original. The result is <b>not</b> cropped, and should have divots on each side.
