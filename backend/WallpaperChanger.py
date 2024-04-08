import ctypes
import os
#image generate
from PIL import Image, ImageDraw
import shutil

class WallpaperChanger:
    def __init__(self, main):
        self.main = main

        self.getDefaultWindowsWallpaper()

    #Точка входа из воркера
    def swapWallpapers(self):
        match self.main.config['MAIN']['mode']:
            case 'auto':
                #Определяем есть ли указанные процессы
                new_state = self.main.support.checkThatTargetProcessesRunning(self.main.config.items('PROCESSES'))

                if new_state == 'no changes':
                    return
            case 'black':
                new_state = 'BLACK'
            case 'default':
                new_state = 'DEFAULT'

        #Определяем и выставляем обои
        if new_state == 'BLACK':
            self.setBlackWallpaper()
        elif new_state == 'DEFAULT':
            self.setDefaultWallpaper()
        else:
            self.setPathAsWallpaper(new_state)     

    def generateBlackWallpaper(self):
        path = f'{self.main.state['transcodedwallpaper_path']}.jpg'

        image = Image.new('RGB', (1, 1), 'black')
        ImageDraw.Draw(image)

        image.save(path)

        return path

    def getDefaultWindowsWallpaper(self, is_force = False):
        if (not os.path.isfile(self.main.config['MAIN']['default_wallpaper']) or is_force):
            
            shutil.copy2(self.main.state['transcodedwallpaper_path'], './AW_default_wallpaper.jpg')

            self.main.config['MAIN']['default_wallpaper'] = './AW_default_wallpaper.jpg'
            self.main.support.writeConfig(self.main.config)

        return

    def changeDefaultWallpaper(self, path_with_file):
        self.main.config['MAIN']['default_wallpaper'] = path_with_file
        self.main.support.writeConfig(self.main.config)

        self.swapWallpapers()

        return
    
    def setBlackWallpaper(self):
        wallpaper = self.generateBlackWallpaper()
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(wallpaper), 3)
        os.remove(wallpaper)

    def setDefaultWallpaper(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(self.main.config['MAIN']['default_wallpaper']), 3)

    def setPathAsWallpaper(self, path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(path), 3)