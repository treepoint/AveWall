import os
import win32com.client
import pyuac

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()
root_folder = scheduler.GetFolder('\\')

class TaskManager:
    def __init__(self, Main):
        self.main = Main

    def addToAutostart(self):
        if not pyuac.isUserAdmin():
            self.main.config['AUTO'] = {
                'action' : 'add'
            }

            self.main.support.writeConfig(self.main.config)
            pyuac.runAsAdmin()
        else:
            task_def = scheduler.NewTask(0)

            location = str(self.main.support.getCurrentPath())

            # Создаем триггер
            TASK_TRIGGER_LOGON = 9
            trigger = task_def.Triggers.Create(TASK_TRIGGER_LOGON)
            trigger.Id = 'LogonTriggerId'
            trigger.UserId = os.environ.get('USERNAME') # получаем имя текущего пользователя
            
            # Добавляем к нему действие
            TASK_ACTION_EXEC = 0
            action = task_def.Actions.Create(TASK_ACTION_EXEC)
            action.ID = self.main.application_name
            action.Path = location + '\\' + f'{self.main.application_name}.exe'
            action.WorkingDirectory = location

            # Выставляем параметры запуска
            task_def.Settings.Enabled = True
            task_def.Settings.Compatibility = 4
            task_def.Settings.ExecutionTimeLimit = 'PT0S'
            task_def.Settings.AllowHardTerminate = True
            task_def.Settings.IdleSettings.StopOnIdleEnd = False
            task_def.Settings.DisallowStartIfOnBatteries = False
            task_def.Settings.StopIfGoingOnBatteries = False
            task_def.Principal.RunLevel = 1

            # Регистрируем таск, если есть — обновляем
            TASK_CREATE_OR_UPDATE = 6
            TASK_LOGON_NONE = 0

            root_folder.RegisterTaskDefinition(
                self.main.application_name,
                task_def,
                TASK_CREATE_OR_UPDATE,
                '',  # Без пользователя
                '',  # Без пароля
                TASK_LOGON_NONE)

    def removeFromAutostart(self):
        if not pyuac.isUserAdmin():
            self.main.config['AUTO'] = {
                'action' : 'delete'
            }

            self.main.support.writeConfig(self.main.config)
            pyuac.runAsAdmin()
        else:
            if self.checkThatAutostartIsActive():
                root_folder.DeleteTask(self.main.application_name, 0)

    # Проверим на наличие таска
    # Да, есть метод получения одного таска по имени, но он падает если таска нет,
    # а завязываться на состояние «я упал» как-то не хочется, потому просто посмотрим
    # в общем списке
    def checkThatAutostartIsActive(self):
        tasks = root_folder.GetTasks(0)
        task_name = self.main.application_name

        is_task_exist = bool(len(list(filter(lambda task: (task.name == task_name), tasks))))

        return is_task_exist
    
    def autostartProcessing(self, autostart_is_on):
        if autostart_is_on == 'add':
            self.addToAutostart()
        
        if autostart_is_on == 'delete':
            self.removeFromAutostart()