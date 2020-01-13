import requests


if __name__ == '__main__':
    movement_path = 'http://192.168.1.16:5000/movement'
    requests.post(movement_path)
