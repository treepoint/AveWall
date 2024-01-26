import os
import sys
#config
import configparser
#Processes
import psutil
#sleep
import time

class Support:
    def __init__(self, setting_file, Main):
        self.settings_file = setting_file
        self.main = Main
    
    def writeConfig(self, config):
        with open(self.settings_file, 'w') as configfile:
            config.write(configfile)

    def createDefaultConfigFile(self):
        config = configparser.ConfigParser()

        config['MAIN'] = {
            'black_wallpaper' : './assets/black.jpg',
            'default_wallpaper' : './assets/default.jpg',
            'polling_timeout' : 1,
            'mode' : 'auto' 
        }

        config['PROCESSES'] = {
            1 : 'change_my_name.exe, ./assets/black.jpg'
        }

        self.writeConfig(config)

        return config

    def readConfig(self):
        config = configparser.ConfigParser()

        #Проверяем, что файл в наличии
        if len(config.read(self.settings_file)) != 1:
            config = self.createDefaultConfigFile()
            config = config.read(self.settings_file)

        return config

    def checkThatTargetProcessesRunning(self, processes):
        running_processes = []

        #Получим все запущенные процессы, искать будем в Python
        for r_process in psutil.process_iter():
            running_processes.append(r_process.name().lower())

        #Если нет — ищем по всему списку
        for process in processes:
            
            process = process[1].split(',')

            if str(process[0]).lower() in running_processes:
                return process[1]
            
            #И небольшая пауза между этим всем, чтобы не было пиковой нагрузки
            time.sleep(0.01)
        
        #Нет так нет
        return False

    def chechDoubledStart(self):
        instance_count = len(list(process for process in psutil.process_iter() 
                                  if process.name() == f'{self.main.application_name}.exe'))
        
        #Основной поток + worker
        if instance_count > 2:
            return True
        else:
            return False
        
    def getCurrentPath(self):
        return os.getcwd()
    
    #Чтобы включать картинки напрямую в аплик
    def resource_path(self, relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)