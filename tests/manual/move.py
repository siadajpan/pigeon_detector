import requests

import settings

if __name__ == '__main__':
    movement_path = settings.Server.MOVEMENT_ADDRESSES[0] + \
                    settings.Server.MOVEMENT
    requests.post(movement_path)
