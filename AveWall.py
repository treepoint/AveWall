from Tray import Tray
from Support import Support
from TaskManager import TaskManager

class WallpaperChanger:
    def __init__(self):
        self.settings_file = 'settings.ini'
        self.application_name = 'AveWall'

        self.support = Support(self.settings_file, self)

        self.task_manager = TaskManager(self)

        self.support.readConfig()
        self.support.generateBlackWallpaper()
        self.support.getDefaultWindowsWallpaper()

        self.config = self.support.returnConfig()
        self.current_state = None

        self.autostart_is_on = self.task_manager.checkThatAutostartIsActive()

        if self.support.autostart_action == 'add':
            self.task_manager.addToAutostart()
        
        if self.support.autostart_action == 'delete':
            self.task_manager.removeFromAutostart()

    def swapWallpapers(self):
        match self.support.mode:
            case 'auto':
                #Определяем есть ли указанные процессы
                new_state = self.support.checkThatTargetProcessesRunning(self.support.target_processes)

                if not new_state:
                    new_state = 'default'
            case 'black':
                new_state = 'black'
            case 'default':
                new_state = 'default'

        if (new_state == self.current_state) and self.current_state is not None:
            return

        #Определяем обои
        if new_state == 'black' and new_state != self.current_state:
            wallpaper = self.support.black_wallpaper
        elif new_state == 'default':
            wallpaper = self.support.default_wallpaper
        else:
            wallpaper = new_state
        
        #Выставляем
        self.support.setWallpaper(wallpaper)

        #Обновляем статус
        self.current_state = new_state

if __name__ == '__main__':
    main = WallpaperChanger()

    if main.support.autostart_action:
        sections = main.support.config.remove_section('AUTO')
        main.support.writeConfig()
    else:
        if not main.support.chechDoubledStart():
            tray = Tray(main)

##TODO:
##Фичи:
#1. Readme при первом запуске
#2. Настройка соответствия аплика и приложения