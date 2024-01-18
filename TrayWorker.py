import time
from PyQt6.QtCore import QThread, pyqtSignal

class TrayWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.app = app_self.main
        self.polling_timeout = self.app.support.polling_timeout

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            self.app.swapWallpapers()
            time.sleep(self.polling_timeout)

    def stop(self):
        self.keepRunning = False