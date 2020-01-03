from threading import Thread
from typing import Callable, List


class DetectionCaller(Thread):
    def __init__(self, process_image_function: Callable, arguments: List,
                 callback: Callable):
        super().__init__()
        self.process_image_function: Callable = process_image_function
        self.arguments = arguments
        self.callback: Callable = callback

    def run(self) -> None:
        detected = self.process_image_function(*self.arguments)
        self.callback(detected)
