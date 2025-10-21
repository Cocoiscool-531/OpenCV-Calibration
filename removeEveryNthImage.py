import os
from glob import glob
from tqdm import tqdm

# Expects images in format img_###.jpg where ### is a number (ex. img_001.jpg)

n = 3
images = glob("calibration/img_*.jpg")

for fName in tqdm(images, unit=" images", desc="Removing"):
    imgNum = int(fName[fName.find("_")+1:fName.find(".jpg")])
    if(imgNum % n != 0):
        newPath = "calibration/ignore" + fName[fName.find("/"):len(fName)]
        os.rename(fName, newPath)
