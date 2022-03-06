import os
import cv2
import configparser
from azure.storage.blob import BlobClient
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')


def main():
    # webカメラから画像の作成
    ret, filedate = generate_temp_image(0)

    # エラー処理(最低限)
    if(not ret):
        print('cant get image!!')
        # 取得できなかった時にSlack SDKに送信する。
    else:
        # azure blobのクライアント作成 (エラー処理必要)
        blob_client = BlobClient.from_connection_string(
            config['azure']['connection'],
            container_name='torinos-image',
            blob_name=f'{filedate}.png')

        # ローカルに一時保存した画像を送信する
        with open(f'{filedate}.png', 'rb') as data:
            blob_client.upload_blob(data)

        # 送信後削除
        os.remove(f'{filedate}.png')


def generate_temp_image(camera_number: int):
    # エラー処理微妙なので見直しが必要か。
    filedate = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    filename = f'{filedate}.png'
    webcamera = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)
    if(webcamera.isOpened()):
        ret, frame = webcamera.read()
        frame = cv2.resize(frame, (640, 480))
        cv2.imwrite(filename, frame)
    else:
        ret = False
    webcamera.release()
    cv2.destroyAllWindows()
    return ret, filedate


if __name__ == '__main__':
    main()
