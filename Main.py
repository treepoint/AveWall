from Tray import Tray
from Support import Support

class WallpaperChanger:
    def __init__(self):
        self.settings_file = 'settings.ini'
        self.support = Support(self.settings_file)

        self.config = self.support.returnConfig()
        self.current_state = False

    def swapWallpapers(self):
        #Определяем есть ли указанные процессы
        new_state = self.support.checkThatTargetProcessesRunning()

        if new_state == self.current_state:
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
    tray = Tray(main)

##TODO:
#1. Автостарт
#2. Дефолтный конфиг
#3. Дефолтные обоины (как дефолтную подтягивать текущую)
#4. Интегрировать все ресурсы прямо в аплик
#5. Добавить кнопку Reload Config
#6. При запуске с уже черной обоиной оно не возвращает на дефолт