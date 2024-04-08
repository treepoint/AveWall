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
#copy
import copy

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
    
    def getProcessDiff(self):
        #pid'ы с прошлого состояния
        prev_pids = copy.copy(self.main.state['prev_pids'])

        #pid'ы что есть сейчас
        current_pids = set(psutil.pids())

        #чуть фильтранем, надеюсь в винде среднем хотя бы 1к служебных процессов
        current_pids = set(filter(lambda x:x >= 1000, current_pids))

        new_diff = set()
        del_diff = set()

        #Находим разницу
        if not prev_pids:
            #Если прошлых pid's нет — значит совсем свежак
            new_diff = current_pids
        else:
            new_diff = current_pids - set(prev_pids)
            del_diff = set(prev_pids) - current_pids

        self.main.state['prev_pids'] = current_pids

        result = {  
                    'new_diff' : new_diff, 
                    'del_diff' : del_diff,
                    'current_pids' : current_pids
                }

        return result
    
    def getStateByProcessCollection(self, processes, pids):
        for process in processes:
                process = process[1].split(',')

                for pid in pids:
                    try:
                        new_process = str(psutil.Process(pid).name()).lower()

                        if new_process == str(process[0]).lower():
                            self.main.state['prev_state_process_PID'] = pid

                            if process[1].replace(' ', '') == 'CUSTOM':
                                return process[2]
                            else:
                                return process[1]
                        
                    #Заглушка, иногда оно путается в показаниях, видимо что-то успевает умереть
                    except psutil.NoSuchProcess:
                        pass

    def getNewStateByProcesses(self, process_diff, processes):
        new_diff = process_diff['new_diff']
        del_diff = process_diff['del_diff']

        is_target_pid_del = False
        new_state = self.main.state['prev_state']

        #Если родились новые процессы
        if len(new_diff) > 0:
            new_pids = list(new_diff)
            new_pids.sort()

            new_state = self.getStateByProcessCollection(processes, new_pids)
   
        #Если какие-то процессы умерли
        if len(del_diff) > 0: 
            del_pids = list(del_diff)
            del_pids.sort()

            for process in processes:
                process = process[1].split(',')

                #Сначала поймем, а наш ли это клиент умер
                is_target_pid_del = False

                for pid in del_pids:
                    try:
                        #Если PID удаленного процесса совпадает с тем, который ранее задавал создание то
                        #Ставим флажок, по которому потом снова пересчитаем новый стейт
                        if self.main.state['prev_state_process_PID'] == pid:
                            is_target_pid_del = True
                    #Заглушка, иногда оно путается в показаниях, видимо что-то успевает умереть
                    except psutil.NoSuchProcess:
                        pass
            
        #Если умер наш клиент или список проверяемых процессов изменился,
        #то тогда прогоняем по всей коллекции процессов
        if is_target_pid_del or self.main.state['prev_processes'] != processes:
            new_state = self.getStateByProcessCollection(processes, process_diff['current_pids'])

        #Пишем коллекцию процессов по которой проверяли как прошлую
        self.main.state['prev_processes'] = processes

        return new_state

    def checkThatTargetProcessesRunning(self, processes):

        process_diff = self.getProcessDiff()
        new_state = self.getNewStateByProcesses(process_diff, processes)

        if not new_state:
            self.main.state['prev_state'] = None
            self.main.state['prev_state_process_PID'] = None
            return 'DEFAULT'

        #Проверяем, что если прошлое состояние осталось таким же как и раньше, то ничего не меняем
        if self.main.state['prev_state'] == new_state:
            return 'no changes'
        else:
        #Иначе меняем записанное прошлое состояние и возвращаем статус
            self.main.state['prev_state'] = new_state
            return new_state

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