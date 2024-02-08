#Tray
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
#Worker
from backend.TrayWorker import TrayWorker
#Interface
from backend.Interface import Interface

class Tray():
    def __init__(self, Main, WallpaperChainger):
        #Главный класс
        self.main = Main
        self.wallpaperChainger = WallpaperChainger

        #Собираем сам трей
        path = self.main.support.resource_path('../AW_assets/icon.png')
        self.icon = Image.open(path)

        #Собираем меню
        self.initMenu()

        self.tray = icon(self.main.application_name, self.icon, menu=self.menu)

        #Запускаем воркер
        self.runWorker()

        #Инициализируем интерфейс
        self.interface = Interface(self)

        #Запускаем трей
        self.tray.run()
    
    def runWorker(self):
        self.tray_worker = TrayWorker(self.main, self.wallpaperChainger)
        self.tray_worker.start()

    def getLocale(self):
        return self.main.config['MAIN']['locale']

    def initMenu(self):
        
        self.menu = menu(
            item(lambda x: 
                    'Запускать вместе с Windows' if self.getLocale() == 'RU' else 'Autostart with Windows', 
                 self.setAutostart, 
                 checked = lambda item: self.main.state['autostart_is_on']), 

            item(lambda x: 'Показать настройки' if self.getLocale() == 'RU' else 'Show settings', 
                 self.showInterface), 

            item(lambda x: 'Режим' if self.getLocale() == 'RU' else 'Mode', 
                menu(item(lambda x: 'Автоматический' if self.getLocale() == 'RU' else 'Auto', 
                         self.setAutoMode, 
                         checked=lambda item: self.main.config['MAIN']['mode'] == 'auto'
                         ), 
                     item(lambda x: 'Обои по умолчанию' if self.getLocale() == 'RU' else 'Default', 
                         self.setDefaultMode, 
                         checked=lambda item: self.main.config['MAIN']['mode'] == 'default'
                         ), 
                     item(lambda x: 'Черный экран' if self.getLocale() == 'RU' else 'Black screen', 
                         self.setBlackMode, 
                         checked=lambda item: self.main.config['MAIN']['mode'] == 'black'
                         ), 
            )), 
            item(lambda x: 'Язык' if self.getLocale() == 'RU' else 'Language', 
                menu(item(lambda x: 'Русский' if self.getLocale() == 'RU' else 'Russian', 
                         self.changeLanguageRU, 
                         checked=lambda item: self.getLocale() == 'RU'
                         ), 
                     item(lambda x: 'Английский' if self.getLocale() == 'RU' else 'English', 
                         self.changeLanguageEN, 
                         checked=lambda item: self.getLocale() == 'EN'
                         ), 
            )), 
            item(lambda x: 'Поставить текущие обои windows как «по умолчанию»' if self.getLocale() == 'RU' else 'Set Windows wallpaper as default', 
                 self.getCurrentWindowsWallpaper), 
            item(lambda x: 'Перезагрузить конфиг' if self.getLocale() == 'RU' else 'Reload config', 
                 self.onConfigReload), 
            item(lambda x: 'Выйти' if self.getLocale() == 'RU' else 'Exit', 
                 self.onExit)
        )

    def changeLanguageRU(self):
        self.changeLanguage('RU')

    def changeLanguageEN(self):
        self.changeLanguage('EN')

    def changeLanguage(self, locale):
        self.main.config['MAIN']['locale'] = locale
        self.main.support.writeConfig(self.main.config)
        self.initMenu()

    def showInterface(self):
        self.interface.open()

    def onExit(self, icon=False, item=False):
        self.tray.stop()

    def onConfigReload(self, icon=False, item=False):
        self.main.config = self.main.support.readConfig()

    def getCurrentWindowsWallpaper(self, icon=False, item=False):
        self.wallpaperChainger.getDefaultWindowsWallpaper(True)

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
        if self.main.state['autostart_is_on']:
            self.main.task_manager.removeFromAutostart()
        else:
            self.main.task_manager.addToAutostart()

        self.main.state['autostart_is_on'] = not self.main.state['autostart_is_on']