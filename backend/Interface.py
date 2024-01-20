import os
import eel

class Interface():
    def __init__(self):
        eel.init('frontend')   

        browserAndMode = self.getBrowserAndMode()

        eel.browsers.set_path(browserAndMode['mode'], browserAndMode['browser_path'])  
        eel.start('index.html', mode=browserAndMode['mode'], size=(400, 600))

    def getBrowserAndMode(self):
        result = {
            'browser_path' : None,
            'mode' : None
        }

        chromium_browser_array = [
            'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            'C:/Program Files/Google/Chrome/Application/chrome.exe'
        ]

        firefox_array = [
            'C:/Program Files (x86)/Google/Mozilla Firefox/Firefox.exe',
            'C:/Program Files/Google/Mozilla Firefox/Firefox.exe'
        ]

        for browser in chromium_browser_array:
            if os.path.isfile(browser):
                result['browser_path'] = browser
                result['mode'] = 'chrome'

                break

        if not result['browser_path']:
            for browser in firefox_array:
                if os.path.isfile(browser):
                    result['browser_path'] = browser
                    result['mode'] = 'chrome-app'

                    break

        return result