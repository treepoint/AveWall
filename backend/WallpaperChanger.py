import ctypes
import os
#image generate
from PIL import Image, ImageDraw
import shutil

class WallpaperChanger:
    def __init__(self, main):
        self.main = main

        self.generateBlackWallpaper()
        self.getDefaultWindowsWallpaper()

        self.current_state = None

    def swapWallpapers(self, is_force = False):
        match self.main.config['MAIN']['mode']:
            case 'auto':
                #Определяем есть ли указанные процессы
                new_state = self.main.support.checkThatTargetProcessesRunning(self.main.config.items('PROCESSES'))

                if not new_state:
                    new_state = 'default'
            case 'black':
                new_state = 'black'
            case 'default':
                new_state = 'default'

        if ((new_state == self.current_state) and self.current_state is not None) and not is_force:
            return

        #Определяем обои
        if new_state == 'black' and new_state != self.current_state:
            wallpaper = self.main.config['MAIN']['black_wallpaper']
        elif new_state == 'default':
            wallpaper = self.main.config['MAIN']['default_wallpaper']
        else:
            wallpaper = new_state
        
        #Выставляем
        self.setWallpaper(wallpaper)

        #Обновляем статус
        self.current_state = new_state

    def setWallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(path), 3)

    def generateBlackWallpaper(self):
        if not os.path.isfile(self.main.config['MAIN']['black_wallpaper']):
            image = Image.new('RGB', (1, 1), 'black')
            ImageDraw.Draw(image)

            image.save(self.main.config['MAIN']['black_wallpaper'])

    def getDefaultWindowsWallpaper(self, is_force = False):
        if (not os.path.isfile(self.main.config['MAIN']['default_wallpaper']) or is_force):
            current_wallpaper_location = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Themes', 'TranscodedWallpaper')
            
            shutil.copy2(current_wallpaper_location, './assets')

            self.main.config['MAIN']['default_wallpaper'] = './assets/default.jpg'
            self.main.support.writeConfig(self.main.config)

        return

    def changeDefaultWallpaper(self, path_with_file):
        self.main.config['MAIN']['default_wallpaper'] = path_with_file
        self.main.support.writeConfig(self.main.config)

        self.swapWallpapers(True)

        return