import requests
from requests.auth import HTTPDigestAuth
import io
from PIL import Image
import numpy as np
import cv2

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
writer1 = cv2.VideoWriter('desktopPC_Dataset_NEW\\5\\above.mp4', fourcc, 6.5, (width, height))
writer2 = cv2.VideoWriter("desktopPC_Dataset_NEW\\5\\diagonal.mp4", fourcc, 6.5, (width, height))

def transform(input):
    img_bin = io.BytesIO(input)
    img_pil = Image.open(img_bin)
    img_np = np.asarray(img_pil)
    image = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
    return image


def main():

    while True:

        # 画像の取得
        rs = requests.get(url, auth=HTTPDigestAuth(user, pswd))
        rs2 = requests.get(url_2, auth=HTTPDigestAuth(user, pswd))

        # 取得した画像データをOpenCVで扱う形式に変換
        image_1 = transform(rs.content)
        image_2 = transform(rs2.content)

        comb_image = cv2.vconcat([image_1, image_2])

        image_resize = cv2.resize(comb_image, dsize=None, fx=0.4, fy=0.4)

        cv2.imshow('image', image_resize)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        writer1.write(image_1)
        writer2.write(image_2)

    writer1.release()
    writer2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
