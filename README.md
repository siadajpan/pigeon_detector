# Pigeon shooter
Software recognising pigeon and starts playing mp3 with crows.
Pigeon recognition may be processed inside main controller unit,
or in a remote server.

Before starting, please download [yolov3.weights](https://drive.google.com/open?id=14X2x7W5tfJRTM7fntA74sGIrb-iaCTp2) into 
```
pigeon_shooter/detection/yolo_coco/
```
## Requirements for other hardware
Install all requirements except picamera from requirements.txt

## Running controller
Run with
 
```bash
python3 run_detection_web_camera.py
```

## Running Server
Run with 

```bash
python3 run_processing_server.py
```
