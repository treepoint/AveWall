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
        path = self.main.support.resource_path('icon.png')
        self.icon = Image.open(path)

        self.menu = menu(
            item('Autostart with Windows', self.setAutostart, checked=lambda item: self.main.autostart_is_on), 
            item('Mode', menu(
                item('Auto', self.setAutoMode), 
                item('Set default', self.setDefaultMode), 
                item('Set black', self.setBlackMode), 
            )), 
            item('Set Windows wallpaper as default', self.getCurrentWindowsWallpaper), 
            item('Reload config', self.onConfigReload), 
            item('Exit', self.onExit)
        )

        self.tray = icon(self.main.application_name, self.icon, menu=self.menu)

        #Запускаем воркер
        self.runWorker()

        #Запускаем трей
        self.tray.run()
    
    def runWorker(self):
        self.tray_worker = TrayWorker(self)
        self.tray_worker.start()

    def onExit(self, icon, item):
        self.tray.stop()

    def onConfigReload(self, icon, item):
        self.main.support.readConfig()

    def getCurrentWindowsWallpaper(self, icon, item):
        self.main.support.getDefaultWindowsWallpaper(True)

    def setAutoMode(self):
        self.setMode('auto')

    def setDefaultMode(self):
        self.setMode('default')

    def setBlackMode(self):
        self.setMode('black')

    def setMode(self, mode):
        self.main.mode = mode
        self.main.support.writeConfig()

    def setAutostart(self):
        if self.main.autostart_is_on:
            self.main.task_manager.removeFromAutostart()
        else:
            self.main.task_manager.addToAutostart()

        self.main.autostart_is_on = not self.main.autostart_is_on