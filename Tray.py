#Tray
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
#Worker
from TrayWorker import TrayWorker

class Tray():
    def __init__(self, Main):
        #Главный класс
        self.main = Main

        #Собираем сам трей
        self.icon = Image.open('icon.png')
        self.menu = menu(item('Exit', self.onCLicked))
        self.tray = icon('wc', self.icon, menu=self.menu)

        #Запускаем воркер
        self.runWorker()

        #Запускаем трей
        self.tray.run()
    
    def onCLicked(self, icon, item):
        self.tray.stop()

    def runWorker(self):
        self.app_worker = TrayWorker(self)
        self.app_worker.start()