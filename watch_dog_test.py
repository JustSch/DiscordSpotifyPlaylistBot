import time
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer



class Auth_File_Event_Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.auth_code_file:
            self.waiting_for_url = False
    def __init__(self):
        self.waiting_for_url = True
        self.auth_code_file = os.path.abspath('auth_code_url.txt')
        super().__init__()

event_handler = Auth_File_Event_Handler()
observer = Observer()
observer.schedule(event_handler, ".", recursive=False) #replace . with full directory at some point
observer.start()

try:
    while event_handler.waiting_for_url:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()

print('file modified')