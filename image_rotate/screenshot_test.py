import pyautogui as pagui
import numpy as np
import time
import datetime

def image_compare(im1, im2):
    return np.array_equal(im1, im2)

if __name__ == '__main__':
    sc_region = (0, 0, 100, 100)
    sc = pagui.screenshot(region=sc_region)
    im1 = np.array(sc)
    while(1):
        sc2 = pagui.screenshot(region=sc_region)
        im2 = np.array(sc2)
        if not np.array_equal(im1, im2):
            now = datetime.datetime.now()
            filename = './output/hik_' + now.strftime('%Y%m%d_%H%M%S') + '.png'
            sc2.save(filename)
            print("Save to File :" + filename)
            im1 = im2
        time.sleep(1)
