import numpy as np
import cv2
import argparse


def loss(coordinate, origin):
    index = (coordinate[0] - 297)**2
    index += (coordinate[1] - 116)**2

    return index


def main(args):
    img = cv2.imread(args.i)

    metric = 100
    best_param = None
    best_metric = 9999999

    while best_metric > 0:
        metric = 0
        rows = img.shape[0]
        blur = 5
        dp = 1

        distconst = 8
        minDist = rows / distconst
        param1 = np.random.randint(20, 100)
        param2 = np.random.randint(20, 100)
        minRadius = np.random.randint(0, 49)
        maxRadius = np.random.randint(1, 50)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, blur)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, minDist,
                                   param1=param1, param2=param2,
                                   minRadius=minRadius, maxRadius=maxRadius)

        if circles is not None:
            circles = np.around(circles)

            metric += (len(circles[0]) - 1) * 9999

            for i in circles[0, :]:
                center = (i[0], i[1])
                metric += loss(center, (args.x, args.y))

        else:
            metric = best_metric

        if metric < best_metric:
            best_metric = metric
            best_param = {'param1': param1,
                          'param2': param2,
                          'distconst': distconst,
                          'minr': minRadius,
                          'maxr': maxRadius}
            print(f'Best metric: {best_metric}, Best param: {best_param}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', required=True, help='')
    parser.add_argument('-x', required=True, help='')
    parser.add_argument('-y', required=True, help='')

    args = parser.parse_args()

    main(args)
