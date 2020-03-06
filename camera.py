import cv2
import numpy as np


def point(img):
    rows = img.shape[0]
    blur = 5
    dp = 1
    distconst = 8
    minDist = rows / distconst
    param1 = 77
    param2 = 19
    minRadius = 8
    maxRadius = 49

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2, 2)

    cv2.imshow('2', gray)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        circles = np.around(circles).astype(int)

        for i in circles[0, :]:
            # center = (i[0], i[1])
            center = (297, 116)
            radius = i[2]

            is_red = colorsegmentation(img, center)

            if is_red:
                cv2.circle(img, center, 2, (255, 255, 0), 1)

    return img


def colorsegmentation(img, center):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    hsv = img_hsv[center[1], center[0]]

    print(hsv)

    if 0 <= hsv[0] <= 60 and 100 <= hsv[1] <= 255 and 0 <= hsv[2] <= 255:
        return True
    else:
        return False


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)

    while capture.isOpened():
        # _, img = capture.read()
        img = cv2.imread('image2.png')

        img = point(img)
        cv2.imshow('test', img)

        if cv2.waitKey(1) != -1:
            break
