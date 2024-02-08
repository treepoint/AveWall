import ctypes
import os
#image generate
from PIL import Image, ImageDraw
import shutil

class WallpaperChanger:
    def __init__(self, main):
        self.main = main

        self.getDefaultWindowsWallpaper()

        self.current_state = None

    def swapWallpapers(self, is_force = False):
        match self.main.config['MAIN']['mode']:
            case 'auto':
                #Определяем есть ли указанные процессы
                new_state = self.main.support.checkThatTargetProcessesRunning(self.main.config.items('PROCESSES'))

                if not new_state:
                    new_state = 'DEFAULT'
            case 'black':
                new_state = 'BLACK'
            case 'default':
                new_state = 'DEFAULT'

        if ((new_state == self.current_state) and self.current_state is not None) and not is_force:
            return

        #Определяем и выставляем обои
        if new_state == 'BLACK' and new_state != self.current_state:
            wallpaper = self.generateBlackWallpaper()
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(wallpaper), 3)
            os.remove(wallpaper)
        elif new_state == 'DEFAULT':
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(self.main.config['MAIN']['default_wallpaper']), 3)
        else:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(new_state), 3)
        
        #Обновляем статус
        self.current_state = new_state

    def generateBlackWallpaper(self):
        path = f'{self.main.state['transcodedwallpaper_path']}.jpg'

        image = Image.new('RGB', (1, 1), 'black')
        ImageDraw.Draw(image)

        image.save(path)

        return path

    def getDefaultWindowsWallpaper(self, is_force = False):
        if (not os.path.isfile(self.main.config['MAIN']['default_wallpaper']) or is_force):
            
            shutil.copy2(self.main.state['transcodedwallpaper_path'], './AW_assets')

            self.main.config['MAIN']['default_wallpaper'] = './AW_assets/default.jpg'
            self.main.support.writeConfig(self.main.config)

        return

    def changeDefaultWallpaper(self, path_with_file):
        self.main.config['MAIN']['default_wallpaper'] = path_with_file
        self.main.support.writeConfig(self.main.config)

        self.swapWallpapers(True)

        return