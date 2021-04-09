import cv2
import numpy as np
import matplotlib.pyplot as plt


def compare(img, sample, high=32, width=8, hist=False, condi=0.5):
    # 儲存指定區塊的sample
    y, x = sample
    s = img[y:y+high, x:x+width]

    # 統計 sample 的 LBP histogram feature vector
    grayscale, count = np.unique(s, return_counts=True)

    # 使用 calcHist() 取得直方圖數據
    s_hist = cv2.calcHist([s], [0], None, [256], [0, 255])

    # 和圖片的每個 high*width 做比較(採用 相關性比較)
    # 將相似度符合的條件畫成同個 color

    # 存放 color 資訊的 陣列
    color = np.zeros(img.shape, dtype=np.uint8)
    # 0 為不塗色, 255 為塗色

    img_y, img_x = img.shape
    for j in range(0, img_y // high):
        for i in range(0, img_x // width):
            y1 = j * high
            y2 = y1 + high
            x1 = i * width
            x2 = x1 + width
            c_hist = cv2.calcHist([img[y1:y2, x1:x2]], [0], None, [256], [0, 255])
            sim = cv2.compareHist(s_hist, c_hist, cv2.HISTCMP_CORREL)

            if sim >= condi:
                color[y1:y2, x1:x2] = 255

    # 繪製 sample LBP 直方圖
    if hist:
        fig = plt.gcf()
        fig.set_size_inches(10, 6)

        plt.title("Local LBP")
        plt.xlabel("Gray Scale")
        plt.ylabel("Count")
        plt.bar(grayscale, count)
        plt.ylim(0, 30)
        plt.xticks(np.linspace(0, 255, 18))
        plt.yticks(np.linspace(0, 30, 7))
        plt.show()

    return color


def bit_to_int(matrix):
    # 傳入 3x3  將二進制值轉成十進制, 傳回十進制值
    pos = np.array([[3, 4, 5], [2, 0, 6], [1, 0, 7]])
    weight = np.power(2, pos)
    lbp_value = np.sum(weight * matrix) - 1
    return lbp_value


def lbp(img):
    # 邊緣填充 0
    y, x = img.shape
    con_img = np.zeros((y+2, x+2), dtype=np.uint16)
    con_img[1:y+1, 1:x+1] = img

    # 儲存 lbp image
    lbp_img = np.zeros(img.shape, dtype=np.uint8)

    # 取值
    for j in range(0, y):
        for i in range(0, x):
            # 取 3x3 區塊
            target = con_img[j:j+3, i:i+3]
            bits = np.where(target >= target[1, 1], 1, 0)
            lbp_img[j, i] = bit_to_int(bits)
    return lbp_img


path = "./road.jpg"
road = cv2.imread(path)

gray = cv2.cvtColor(road, cv2.COLOR_BGR2GRAY)

# 利用 LBP 特徵來做出 markers
road_lbp = lbp(gray)
# cv2.imshow("road_lbp", road_lbp)


fg = compare(road_lbp, sample=(880, 90), high=64, width=32, condi=0.84)
# print(np.unique(fg, return_counts=True))
# cv2.imshow("fg", fg)

# watershed
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thres = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
mb = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel, iterations=2)
bg = cv2.dilate(mb, kernel, iterations=3)
# cv2.imshow("bg", bg)

unknown = cv2.subtract(bg, fg)
# cv2.imshow("unknown", unknown)

_, markers = cv2.connectedComponents(fg)
print(np.unique(markers, return_counts=True))
markers = cv2.watershed(road, markers=markers)
road[markers == -1] = [0, 0, 0]
# cv2.imshow("watershed", road)

# draw
color_block = np.zeros(road.shape, dtype=np.uint8)
color_block[markers == 0] = [255, 255, 255]
color_block[markers == 1] = [191,  62, 255]
color_block[markers == 2] = [130, 130, 130]
color_block[markers == 3] = [152, 251, 152]
# cv2.imshow("color_block", color_block)

# result
result = cv2.addWeighted(road, 1, color_block, 0.8, 0)

cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
