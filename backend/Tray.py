#Tray
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
#Worker
from backend.TrayWorker import TrayWorker
#Interface
from backend.Interface import Interface
import eel

class Tray():
    def __init__(self, Main, WallpaperChainger):
        #Главный класс
        self.main = Main
        self.wallpaperChainger = WallpaperChainger

        #Собираем сам трей
        path = self.main.support.resource_path('../assets/icon.png')
        self.icon = Image.open(path)

        self.menu = menu(
            item('Autostart with Windows', self.setAutostart, checked=lambda item: self.main.autostart_is_on), 
            item('Show', self.showInterface), 
            item('Mode', menu(
                item('Auto', 
                      self.setAutoMode, 
                      checked=lambda item: self.main.config['MAIN']['mode'] == 'auto'
                    ), 
                item('Set default', 
                      self.setDefaultMode, 
                      checked=lambda item: self.main.config['MAIN']['mode'] == 'default'
                    ), 
                item('Set black', 
                      self.setBlackMode, 
                      checked=lambda item: self.main.config['MAIN']['mode'] == 'black'
                    ), 
            )), 
            item('Set Windows wallpaper as default', self.getCurrentWindowsWallpaper), 
            item('Reload config', self.onConfigReload), 
            item('Exit', self.onExit)
        )

        self.tray = icon(self.main.application_name, self.icon, menu=self.menu)

        #Запускаем воркер
        self.runWorker()

        #Прокидываем функции из Pyhton в eel
        eel._expose("setBlackMode", self.setBlackMode)
        eel._expose("setDefaultMode", self.setDefaultMode)

        #Запускаем трей
        self.tray.run()
    
    def runWorker(self):
        self.tray_worker = TrayWorker(self.main, self.wallpaperChainger)
        self.tray_worker.start()

    def showInterface(self):
        #Запускаем интерфейс
        interface = Interface()

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
        self.main.config['MAIN']['mode'] = mode
        self.main.support.writeConfig(self.main.config)

    def setAutostart(self):
        if self.main.autostart_is_on:
            self.main.task_manager.removeFromAutostart()
        else:
            self.main.task_manager.addToAutostart()

        self.main.autostart_is_on = not self.main.autostart_is_on