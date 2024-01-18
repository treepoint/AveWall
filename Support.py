import os
import ctypes
#config
import configparser
#Processes
import psutil
#sleep
import time
#image generate
from PIL import Image, ImageDraw
import shutil
import sys

class Support:
    def __init__(self, setting_file):
        self.settings_file = setting_file

        self.last_detected_process = None

    def returnConfig(self):
        return self.config 
    
    def writeConfig(self):
        with open(self.settings_file, 'w') as configfile:
            self.config.write(configfile)

    def createDefaultConfigFile(self):
        self.config = configparser.ConfigParser()

        self.config['MAIN'] = {
            'black_wallpaper' : 'black.jpg',
            'default_wallpaper' : 'default.jpg',
            'polling_timeout' : 1
        }

        self.config['PROCESSES'] = {
            1 : 'change_my_name.exe'
        }

        self.writeConfig()

    def readConfig(self):
        self.config = configparser.ConfigParser()

        #Проверяем, что файл в наличии
        if len(self.config.read(self.settings_file)) != 1:
            self.createDefaultConfigFile()
            self.config.read(self.settings_file)

        #Парсим основные параметры
        self.polling_timeout = int(self.config['MAIN']['polling_timeout'])
        self.default_wallpaper = self.config['MAIN']['default_wallpaper']
        self.black_wallpaper = self.config['MAIN']['black_wallpaper']

        #Парсим список процессов
        self.target_processes = []
        processes = self.config.items('PROCESSES')

        for key, process in processes:
            self.target_processes.append(process)

    def checkThatTargetProcessesRunning(self, target_processes):
        running_processes = []
        
        #Получим все запущенные процессы, искать будем в Python
        for r_process in psutil.process_iter():
            running_processes.append(r_process.name())

        #Проверим не работает ли прошлый процесс
        if self.last_detected_process:
            if self.last_detected_process in running_processes:
                return True

        #Если нет — ищем по всему списку
        for process in target_processes:
            if process in running_processes:
                self.last_detected_process = process
                return True
            
            #И небольшая пауза между этим всем, чтобы не было пиковой нагрузки
            time.sleep(0.05)
        
        #Нет так нет
        self.last_detected_process = False
        return False
    
    def setWallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(path), 3)

    def chechDoubledStart(self):
        instance_count = len(list(process for process in psutil.process_iter() 
                                  if process.name() == 'AveWall.exe'))
        
        #Основной поток + worker
        if instance_count > 2:
            return True
        else:
            return False
        
    def generateBlackWallpaper(self):
        if not os.path.isfile(self.black_wallpaper):
            image = Image.new('RGB', (1, 1), 'black')
            ImageDraw.Draw(image)

            image.save(self.black_wallpaper)

    def getDefaultWindowsWallpaper(self, is_force = False):
        if (not os.path.isfile(self.default_wallpaper) or is_force):
            current_wallpaper_location = os.path.join(os.getenv('APPDATA'), 'Microsoft/Windows/Themes', 'TranscodedWallpaper')

            shutil.copy2(current_wallpaper_location, self.default_wallpaper)  
        
    def getCurrentPath(self):
        return os.getcwd()
    
    #for including resources directly at application
    def resource_path(self, relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)