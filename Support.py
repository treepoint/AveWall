import os
import ctypes
#config
import configparser
#Processes
import psutil
#sleep
import time

class Support:
    def __init__(self, setting_file):
        self.settings_file = setting_file

        self.readConfig()
        self.last_detected_process = None

    def returnConfig(self):
        return self.config 

    def writeConfig(self):
        with open(self.settings_file, 'w') as configfile:
            self.config.write(configfile)

    def readConfig(self):
        self.config = configparser.ConfigParser()
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
        if self.checkThatTargetProcessesRunning(['svchost.exe']):
            return True
        else:
            return False
        
    def getCurrentPath():
        return os.getcwd()