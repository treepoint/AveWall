#Tray
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
#Worker
from TrayWorker import TrayWorker

class Tray():
    def __init__(self, Main):
        #Главный класс
        self.main = Main

        #Собираем сам трей
        self.icon = Image.open('icon.png')

        self.menu = menu(
            item('Set Windows wallpaper as default', self.getCurrentWindowsWallpaper), 
            item('Reload config', self.onConfigReload), 
            item('Exit', self.onExit)
        )

        self.tray = icon('AveWall', self.icon, menu=self.menu)

        #Запускаем воркер
        self.runWorker()

        #Запускаем трей
        self.tray.run()
    
    def onExit(self, icon, item):
        self.tray.stop()

    def onConfigReload(self, icon, item):
        self.main.support.readConfig()

    def getCurrentWindowsWallpaper(self, icon, item):
        self.main.support.getDefaultWindowsWallpaper(True)

    def runWorker(self):
        self.app_worker = TrayWorker(self)
        self.app_worker.start()