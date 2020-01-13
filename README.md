# Pigeon shooter
Software recognising pigeon and starts playing mp3 with crows noise
and send request for other controller to start moving plastic bird.
There may be one or two Raspberry Pi controllers in use. One for 
recognition task, the other for moving task. Both of the tasks can be
also run in one controller

## Movement controller
Movement controller is located at
```movement_controller/movement_controller.py```
and run with

```bash
python3 run_movement_server.py
```

The main task for that unit is controlling a servo that is moving the 
plastic bird, or some other scary object. I used Rasbperry Pi and 
controlling its GPIO. For now, no other controller can be used for that
task.
Controller is running
a Flask server so it can be run on the same Raspberry Pi as the main
recognition controller.
In ```settings.py``` there are some configuration e.g. IP address
of the movement controller. 

## Recognition controller
Recognition controller is making pictures and comparing them looking 
for some movement. Once movement occur, controller sends the movement 
frame to detection controller. If the bird is recognised, recognition
controller starts playing mp3 from ```master_controller/files/```
and sends the request to the movement controller to start moving
the servo.

### Simple Recognition
By default, simple recognition controller is used. Simple recognizer 
just checks if movement frame is within some dimensions without
analyzing the frame. Any small enough movement
on the picture can trigger the recognition. This is usually good enough.

### YOLO recognition
If you want to use Yolo detector, please download 
[yolov3.weights](https://drive.google.com/open?id=14X2x7W5tfJRTM7fntA74sGIrb-iaCTp2) into 
```
pigeon_shooter/detection/yolo_coco/
```
and update inside ```master_controller/detection_runners/local_detection_runner.py```
changing ```SimpleDetector()``` into ```YOLODetector()```. 
Yolo detector is much slower, and does not always trigger detection 
when birds are present on the obscured picture. Yolo detector is not always 
working well for some worse cameras or birds that are far away.

### Detection on different machine
Yolo detector is slow on Rasbperry Pi (on RasPi 4.0 it takes
about 20s for a picture). There is possibility to run YOLO detector 
on a more powerful computer connected to the same network. Movement 
frame is sent to that server and gets a bool response about birds 
detection.
To use some other machine to run detection, download the project to the 
other machine, together with weights and run
```bash
python3 run_processing_server.py
```
Update ```settings.py``` with the ip address of the processing server
on the Raspberry Pi controller.
Every time, detection happens, controller checks for presence of 
some non-local processing server. If there is one, it sends the frame 
 to it. Otherwise, it uses local detector.

## Requirements for
Install all requirements except picamera from requirements.txt

## Running controller
Run with
 
```bash
python3 run_detection_web_camera.py
```
