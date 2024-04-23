import time
from PyQt5.QtCore import QThread, pyqtSignal

class TrayWorker(QThread):
    def __init__(self, main, wallpaperChainger):
        super().__init__()

        self.main = main
        self.wallpaperChainger = wallpaperChainger

        self.polling_timeout = int(self.main.config['MAIN']['polling_timeout'])

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            self.wallpaperChainger.swapWallpapers()
            time.sleep(self.polling_timeout)

    def stop(self):
        self.keepRunning = False