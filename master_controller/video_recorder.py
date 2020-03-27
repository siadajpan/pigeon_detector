import datetime
import os

import cv2


class VideoRecorder:
    def __init__(self):
        self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.video_writer = None

    def create_folder_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def create_folder_structure(self):
        date = datetime.datetime.now()
        dir_path = f"{date.year}-{date.month}-{date.day}"
        video_name = f"{date.hour}-{date.minute}-{date.second}.avi"

        self.create_folder_if_not_exists(dir_path)
        video_path = os.path.join(dir_path, video_name)

        return video_path

    def init_recording(self, frame, fps):
        video_path = self.create_folder_structure()
        h, w = frame.shape[:2]

        self.video_writer = cv2.VideoWriter(video_path, self.codec, fps, (w, h))

    def update_frame(self, frame):
        self.video_writer.write(frame)

    def stop_recording(self):
        self.video_writer.release()
