import cv2 as cv
import os
from PIL import ImageGrab
import numpy as np

VIDEO_STREAM = 0

FILES = 1

DESKTOP = 2


def video_stream(video):
    state, frame = video.read()
    if state is True:
        return frame
    else:
        print('capture error')
        return None


def files(obj, url, max_frame):
    file_name = url + str(obj.index % max_frame) + '.png'
    obj.index += 1
    if os.path.exists(file_name):
        img = cv.imread(file_name)
        return img
    else:
        print('capture error')
        return None


def desktop(box):
    img = ImageGrab.grab(box)
    if img:
        img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        return img
    else:
        print('capture error')
        return None


class VideoStream:

    def __init__(self, mode, max_frame=None, url=None):

        if mode == VIDEO_STREAM:
            video = cv.VideoCapture(url)
            self._args = (video,)
            self._target = video_stream

        elif mode == FILES:
            self.index = 1
            self.url = url
            self.max = max_frame
            if os.path.exists(url) is False:
                print('folder not found')
            self._args = (self, self.url, self.max)
            self._target = files

        elif mode == DESKTOP:
            self.box = (200, 200, 750, 480)
            print('please select the screen, then enter key t to finish')
            while True:
                img = ImageGrab.grab(self.box)
                img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
                cv.imshow('select', img)
                if cv.waitKey(1) == 116:
                    cv.destroyAllWindows()
                    break

            self._args = (self.box,)
            self._target = desktop
            print('select screen successful')

        else:
            print('parameter error')

    # 获取图像
    def get_frame(self):
        frame = self._target(*self._args)
        return frame
