import os

#eel fix
import sys, io
if hasattr(sys, "_MEIPASS"):
    buffer = io.StringIO()
    sys.stdout = sys.stderr = buffer

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

        self.state['prev_pids'] = None
        self.state['prev_state'] = None
        self.state['prev_processes'] = None
        self.state['prev_state_process_PID'] = None
        self.state['excluded_pids'] = []
        self.state['checked_pids'] = []
         
        #Обрабатываем автостарт
        self.task_manager = TaskManager(self)
        self.state['autostart_is_on'] = self.task_manager.checkThatAutostartIsActive()
        self.state['transcodedwallpaper_path'] = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Themes', 'TranscodedWallpaper')

        self.task_manager.autostartProcessing()

if __name__ == '__main__':
    #hardcoded exception just for avoid crushes at exceptional situations
    try:
        main = Main()
        wallpaperChainger = WallpaperChanger(main)

        if main.config.has_option('AUTO','action'):
            main.config.remove_section('AUTO')
            
            main.support.writeConfig(main.config)
        else:
            if not main.support.chechDoubledStart():
                tray = Tray(main, wallpaperChainger)
    except Exception as error:
        print(f'unhandled error occur: {error}')
