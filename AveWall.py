from backend.Tray import Tray
from backend.WallpaperChanger import WallpaperChanger
from backend.TaskManager import TaskManager
from backend.Support import Support

class Main():
    def __init__(self):
        self.settings_file = 'settings.ini'
        self.application_name = 'AveWall'

        self.support = Support(self.settings_file, self)
        self.config = self.support.readConfig()

        #Глобальное состояние
        self.state = {}

        #Обрабатываем автостарт
        self.task_manager = TaskManager(self)
        self.state['autostart_is_on'] = self.task_manager.checkThatAutostartIsActive()
        
        self.task_manager.autostartProcessing()

if __name__ == '__main__':
    main = Main()
    wallpaperChainger = WallpaperChanger(main)

    if main.config.has_option('AUTO','action'):
        main.config.remove_section('AUTO')
        
        main.support.writeConfig(main.config)
    else:
        if not main.support.chechDoubledStart():
            tray = Tray(main, wallpaperChainger)

##TODO:
##Фичи:
#1. Black не генерировать, а сразу писать напрямую в папку винды (опционально)
            
##Отладка
#1. Оптимизации (лаги в A Plague Tale)
#2. Адаптивная таблица при переключении языков