import os
import eel
import json
import ctypes
from tkinter import *
from tkinter import filedialog
user32 = ctypes.windll.user32

class Interface():
    def __init__(self, tray):
        eel.init('frontend')   

        self.browserAndMode = self.getBrowserAndMode()

        self.tray = tray

        #Прокидываем функции из Python в eel
        eel._expose("getConfig", self.returnConfig)
        eel._expose("getState", self.returnState)

        #Настройки
        eel._expose("setAutostart", self.tray.setAutostart)
        eel._expose("changeDefaultWallpaper", self.tray.wallpaperChainger.changeDefaultWallpaper)

        #Процессы
        eel._expose("saveProcesses", self.saveProcesses)

        #Mode
        eel._expose("setAutoMode", self.tray.setAutoMode)
        eel._expose("setDefaultMode", self.tray.setDefaultMode)
        eel._expose("setBlackMode", self.tray.setBlackMode)

        #actions
        eel._expose("onConfigReload", self.tray.onConfigReload)
        eel._expose("getCurrentWindowsWallpaper", self.tray.getCurrentWindowsWallpaper)
        eel._expose("onExit", self.tray.onExit)

        #Файлы
        eel._expose("getFileWithPath", self.getFileWithPath)

        eel.browsers.set_path(self.browserAndMode['mode'], self.browserAndMode['browser_path'])  

    def getBrowserAndMode(self):
        result = {
            'browser_path' : None,
            'mode' : None
        }

        chromium_browser_array = [
            'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            'C:/Program Files/Google/Chrome/Application/chrome.exe',
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        ]

        firefox_array = [
            'C:/Program Files/Google/Mozilla Firefox/Firefox.exe',
            'C:/Program Files (x86)/Google/Mozilla Firefox/Firefox.exe'
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
        width = 694

        basic_height = 550
        height = min(1280, basic_height + 44*len(self.tray.main.config['PROCESSES']))

        eel.start('index.html', 
                   mode=self.browserAndMode['mode'], 
                   size=(width, height), 
                   position=((user32.GetSystemMetrics(0)-width)/2, (user32.GetSystemMetrics(1)-height)/2)
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
    
    def saveProcesses(self, processes_json):
        processes = {}

        for process in processes_json['items']:
            processes[process['id']] = f'{process['name']}, {process['type']}, {process['wallpaper']}'

        self.tray.main.config['PROCESSES'] = processes
            
        self.tray.main.support.writeConfig(self.tray.main.config)

    def getFileWithPath(self, type):
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)

        if type == 'image':
            path = filedialog.askopenfilename(filetypes=[("Image File",'.jpg .png .jpeg')])
            return path
        
        if type == 'exe':
            path = filedialog.askopenfilename(filetypes=[("Applications", "*.exe")])
            return path

        return None