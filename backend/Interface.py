import os
import eel
import json
import ctypes
user32 = ctypes.windll.user32

class Interface():
    def __init__(self, tray):
        eel.init('frontend')   

        self.browserAndMode = self.getBrowserAndMode()

        self.tray = tray

        #Прокидываем функции из Python в eel
        eel._expose("getConfig", self.returnConfig)
        eel._expose("getState", self.returnState)

        #Автостарт
        eel._expose("setAutostart", self.tray.setAutostart)

        #Mode
        eel._expose("setAutoMode", self.tray.setAutoMode)
        eel._expose("setDefaultMode", self.tray.setDefaultMode)
        eel._expose("setBlackMode", self.tray.setBlackMode)

        #actions
        eel._expose("onConfigReload", self.tray.onConfigReload)
        eel._expose("getCurrentWindowsWallpaper", self.tray.getCurrentWindowsWallpaper)
        eel._expose("onExit", self.tray.onExit)

        eel.browsers.set_path(self.browserAndMode['mode'], self.browserAndMode['browser_path'])  

    def getBrowserAndMode(self):
        result = {
            'browser_path' : None,
            'mode' : None
        }

        chromium_browser_array = [
            'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            'C:/Program Files/Google/Chrome/Application/chrome.exe'
        ]

        firefox_array = [
            'C:/Program Files (x86)/Google/Mozilla Firefox/Firefox.exe',
            'C:/Program Files/Google/Mozilla Firefox/Firefox.exe'
        ]

        for browser in chromium_browser_array:
            if os.path.isfile(browser):
                result['browser_path'] = browser
                result['mode'] = 'chrome'

                break

        if not result['browser_path']:
            for browser in firefox_array:
                if os.path.isfile(browser):
                    result['browser_path'] = browser
                    result['mode'] = 'chrome-app'

                    break

        return result
    
    def open(self):
        width = 500
        height = 700
        eel.start('index.html', 
                   mode=self.browserAndMode['mode'], 
                   size=(width, height), 
                   position=((user32.GetSystemMetrics(0)-width)/2, (user32.GetSystemMetrics(1)-600)/2)
                )

    def returnState(self):
        return json.dumps(self.tray.main.state)

    def returnConfig(self):
        result = {}

        sections=self.tray.main.config.sections()

        for section in sections:
            items=self.tray.main.config.items(section)
            result[section]=dict(items)

        result=json.dumps(result)

        return result