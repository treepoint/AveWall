from Tray import Tray
from Support import Support

class WallpaperChanger:
    def __init__(self):
        self.settings_file = 'settings.ini'
        self.support = Support(self.settings_file)

        self.config = self.support.returnConfig()
        self.current_state = None

    def swapWallpapers(self):
        #Определяем есть ли указанные процессы
        new_state = self.support.checkThatTargetProcessesRunning(self.support.target_processes)

        if (new_state == self.current_state) and self.current_state is not None:
            return

        #Определяем обои
        if new_state and new_state != self.current_state:
            wallpaper = self.support.black_wallpaper
        else:
            wallpaper = self.support.default_wallpaper
        
        #Выставляем
        self.support.setWallpaper(wallpaper)

        #Обновляем статус
        self.current_state = new_state

if __name__ == '__main__':
    main = WallpaperChanger()

    if not main.support.chechDoubledStart():
        tray = Tray(main)

##TODO:
#Deploy
#1. Дефолтный конфиг
#2. Дефолтные обоины (как дефолтную подтягивать текущую)
#3. Интегрировать все ресурсы прямо в аплик
        
##Фичи:
#1. Свои обои для каждого аплика
#2. Автостарт
#3. Брать дефолтную обоину из текущих, а черную — генерировать