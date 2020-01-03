import cv2
import requests


addr = 'http://localhost:5000'
send_pic_address = addr + '/process_image'

image_ = cv2.imread('/home/karol/Documents/auto.png')
_, img_encoded = cv2.imencode('.jpg', image_)

if __name__ == '__main__':
    try:
        response = requests.post(send_pic_address, img_encoded.tostring())
        print(response.json())
    except requests.exceptions.ConnectionError:
        print('cant connect')

