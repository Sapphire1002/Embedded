import cv2
import numpy as np


def nothing(x):
    pass


def output_img(img, text):
    cv2.namedWindow(text, cv2.WINDOW_NORMAL)
    cv2.imshow(text, img)
    cv2.imwrite('%s.png' % text, img)


# read image
path = "E:/MyProgramming/Python/Practice/opencv_practice/road/road.jpg"
road = cv2.imread(path)
# print(road.shape)  # (1000, 1000, 3)

# convert to gray
gray = cv2.cvtColor(road, cv2.COLOR_BGR2GRAY)
# output_img(gray, text="./road/gray")

# filter
blur = cv2.GaussianBlur(gray, (5, 5), 0)
# output_img(blur, text='./road/5x5blur')

# adjustment canny
# cv2.namedWindow("Canny")
# cv2.createTrackbar('thres1', 'Canny', 70, 255, nothing)
# cv2.createTrackbar('thres2', 'Canny', 210, 255, nothing)
#
# while True:
#     thres1 = cv2.getTrackbarPos('thres1', 'Canny')
#     thres2 = cv2.getTrackbarPos('thres2', 'Canny')
#     edge_canny = cv2.Canny(blur, thres1, thres2)
#     cv2.imshow('original', road)
#     cv2.imshow('Canny', edge_canny)
#     if cv2.waitKey(1) == ord('q'):
#         break

# test canny
# edge_test = cv2.Canny(gray, 150, 255)
# output_img(edge_test, text='./road/gray_canny_150_255')

# sobel
sobel = cv2.Sobel(gray, ddepth=-1, dx=1, dy=0, ksize=3)
# output_img(sobel, text='./road/sobel_dx')

# adjustment threshold
# cv2.namedWindow("threshold")
# cv2.createTrackbar('thres', 'threshold', 70, 255, nothing)
#
# while True:
#     thresh = cv2.getTrackbarPos('thres', 'threshold')
#     _, my_thres = cv2.threshold(sobel, thresh, 255, cv2.THRESH_BINARY)
#     cv2.imshow('original', sobel)
#     cv2.imshow('threshold', my_thres)
#     if cv2.waitKey(1) == ord('q'):
#         break

# threshold
_, thres = cv2.threshold(sobel, 30, 255, cv2.THRESH_BINARY)
# output_img(thres, text='./road/gray_thres_30_255')

# line detection: HoughLines or HoughLinesP
# adjustment HoughLinesP
# cv2.namedWindow("HoughLinesP", cv2.WINDOW_NORMAL)
# cv2.createTrackbar("line_thres", "HoughLinesP", 100, 500, nothing)
# cv2.createTrackbar("min_line", "HoughLinesP", 100, 500, nothing)
# cv2.createTrackbar("max_gap", "HoughLinesP", 1, 100, nothing)
#
# while True:
#     line_thres = cv2.getTrackbarPos("line_thres", "HoughLinesP")
#     min_line = cv2.getTrackbarPos("min_line", "HoughLinesP")
#     max_gap = cv2.getTrackbarPos("max_gap", "HoughLinesP")
#
#     linesP = cv2.HoughLinesP(
#         image=thres,
#         rho=1,
#         theta=np.pi/180,
#         threshold=line_thres,
#         minLineLength=min_line,
#         maxLineGap=max_gap
#     )

#     try:
#         road_cp = road.copy()
#         for line in linesP:
#             for x1, y1, x2, y2 in line:
#                 cv2.line(road_cp, (x1, y1), (x2, y2), (255, 0, 0), 5)
#
#         cv2.imshow("HoughLinesP", road_cp)
#         if cv2.waitKey(1) == ord('q'):
#             break
#
#     except TypeError:
#         cv2.setTrackbarPos("line_thres", "HoughLinesP", 100)
#         cv2.setTrackbarPos("min_line", "HoughLinesP", 100)
#         cv2.setTrackbarPos("max_gap", "HoughLinesP", 1)
#         continue

# test HoughLinesP
line_thres = 375
min_line = 489
max_gap = 60
linesP = cv2.HoughLinesP(thres, 1, np.pi/180, threshold=line_thres, minLineLength=min_line, maxLineGap=max_gap)
print(linesP.shape)
print(linesP)

crop = road.copy()
for line in linesP:
    for x1, y1, x2, y2 in line:
        cv2.line(road, (x1, y1), (x2, y2), (255, 0, 0), 5)
# [[[509 629 998 857]]
#
#  [[  3 843 509 628]]]

# cropped image


# last:
# original -> gray -> sobel(ddpeth=-1, dx=1, dy=0, ksize=3) -> threshold(30, 255, THRESH_BINARY) ->
# HoughLinesP(1, np.pi/180, threshold=375, minLineLength=489, maxLineGap=60)

# cv2.imshow("Linear", road)
# cv2.imwrite("./road/road_result.png", road)
cv2.waitKey(0)
cv2.destroyAllWindows()
