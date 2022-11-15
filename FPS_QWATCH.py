import requests
from requests.auth import HTTPDigestAuth
import io
from PIL import Image
import numpy as np
import cv2
import time

# カメラのIPアドレス　192.168.11.43
# 画像データの取得　　/cgi-bin/camera
# 解像度の指定　　　　resolution
# url = "qhttp://192.168.11.43/cgi-bin/camera?resolution=1280"

# url = "http://133.91.72.35:50826/snapshot.jpg?dummy=1609932222870"
url = "http://133.91.72.35:50826/snapshot.jpg?dummy=1609932267801"
url_2 = "http://133.91.72.32/snapshot.jpg?dummy=1624535628134"

# 認証情報
user = "admin"
pswd = "umelab1121"

# 画像の取得
rs = requests.get(url, auth=HTTPDigestAuth(user, pswd))

# 取得した画像データをOpenCVで扱う形式に変換
img_bin = io.BytesIO(rs.content)
img_pil = Image.open(img_bin)
img_np = np.asarray(img_pil)
image = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)

height, width, channels = image.shape[:3]
print("width:{} height:{}".format(width, height))

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('00011.mp4', fourcc, 10, (width, height))




def transform(input):
    img_bin = io.BytesIO(input)
    img_pil = Image.open(img_bin)
    img_np = np.asarray(img_pil)
    image = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
    return image


def main():

    frame_all = 0

    # 開始時間
    start = time.time()

    while True:

        # 画像の取得
        rs = requests.get(url, auth=HTTPDigestAuth(user, pswd))
        rs2 = requests.get(url_2, auth=HTTPDigestAuth(user, pswd))

        # 取得した画像データをOpenCVで扱う形式に変換
        image = transform(rs.content)
        image_2 = transform(rs2.content)

        image_resize = cv2.resize(image, dsize=None, fx=0.5, fy=0.5)
        image_resize2 = cv2.resize(image_2, dsize=None, fx=0.5, fy=0.5)

        cv2.imshow('image', image_resize)
        cv2.imshow('image_2', image_resize2)

        frame_all = frame_all + 1

        print(frame_all)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 終了時間
    end = time.time()

    # Time elapsed
    seconds = end - start
    print("経過時間: {0} seconds".format(seconds))

    print("Frame:", frame_all)

    # Calculate frames per second
    fps = frame_all / seconds
    print("計算したFPS : {0}".format(fps))


if __name__ == "__main__":
    main()

# 1280×720: 18.1[FPS]
# 1920×1080: 10[FPS]