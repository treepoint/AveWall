import os
import sys
#config
import configparser
#Processes
import psutil
#sleep
import time
#system language
import locale

class Support:
    def __init__(self, setting_file, Main):
        self.settings_file = setting_file
        self.main = Main
    
    def writeConfig(self, config):
        with open(self.settings_file, 'w', encoding="utf-8") as configfile:
            config.write(configfile)

    def createDefaultConfigFile(self):
        config = configparser.ConfigParser()

        config['MAIN'] = {
            'default_wallpaper' : './AW_default_wallpaper.jpg',
            'polling_timeout' : 1,
            'mode' : 'auto',
            'locale' : self.getCurrentSystemLanguage()
        }

        config['PROCESSES'] = {
            1 : 'change_my_name.exe,DEFAULT,'
        }

        self.writeConfig(config)

    def readConfig(self):
        config = configparser.ConfigParser()

        #Проверяем, что файл в наличии
        if len(config.read(self.settings_file, encoding='utf-8')) != 1:
            self.createDefaultConfigFile()
            config = self.readConfig()

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
                if process[1].replace(' ', '') == 'CUSTOM':
                    return process[2]
                else:
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
        if not hasattr(sys, "_MEIPASS"):
            return relative_path
        
        else:
            base_path = getattr(
                sys,
                '_MEIPASS',
                os.path.dirname(os.path.abspath(__file__)))
            
            return os.path.join(base_path, relative_path)
    
    def getCurrentSystemLanguage(self):
        current_locale = locale.getdefaultlocale()[0]

        if 'ru' in current_locale:
            return 'RU'
        else:
            return 'EN'