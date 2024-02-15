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
        prev_pids = self.main.state['prev_pids']

        #Если прошлых pid's нет — значит совсем свежак
        if not prev_pids:
            self.main.state['prev_pids'] = psutil.pids()
            return
                        
        #При включение-выключении одного процесса все круто, но нам надо еще смотреть по приоритетам.
        #То есть каждый раз, даже если процесс еще работает, нам надо смотреть по разнице pid'ов, не появился ли
        #молодой человечек круче нашего текущего, который бы переопределял обоину
        current_pids = psutil.pids()
        new_pids = set(current_pids) - set(prev_pids)

        if new_pids:
            new_pids = list(new_pids)
            new_pids.sort()

            for process in processes:
                process = process[1].split(',')

                for pid in new_pids:
                    try:
                        new_process = str(psutil.Process(pid).name()).lower()
                    
                        if new_process == str(process[0]).lower():
                            if process[1].replace(' ', '') == 'CUSTOM':
                                return process[2]
                            else:
                                return process[1]
                        
                    #Заглушка, иногда оно путается в показаниях, видимо что-то успевает умереть
                    except psutil.NoSuchProcess:
                        pass

        self.main.state['prev_pids'] = current_pids
        
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
        

    def wait_for_process_by_name(name, poll_interval=0.1, timeout=None):
        """Wait for process with name "name" to be started
        and return a Process() instance when this happens.

        If "timeout" is specified OSError is raised if the process
        doesn't appear within the time specified, which is expressed
        in seconds.
        """
        if timeout is not None:
            raise_at = time.time() + timeout
        else:
            raise_at = None
        while 1:
            pids1 = psutil.get_pid_list()
            time.sleep(poll_interval)
            pids2 = psutil.get_pid_list()
            new_pids = set(pids2) - set(pids1)
            if new_pids:
                new_pids = list(new_pids)
                new_pids.sort()
                for pid in new_pids:
                    print(psutil.Process(pid).name)
                    try:
                        p = psutil.Process(pid)
                    except psutil.NoSuchProcess:
                        # process is dead in meantime
                        continue
                    else:
                        if p.name == name:
                            return p
            if raise_at is not None and time.time() >= raise_at:
                raise OSError("timeout")