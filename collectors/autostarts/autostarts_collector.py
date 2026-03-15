import winreg
import os

class AutostartsCollector:
    def __init__(self):
        pass
    

    def get_registry_autostarts(self):
      path = r"Software\Microsoft\Windows\CurrentVersion\Run"

      key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)

      i = 0
      autostarts = []

      while True:
          try:
              # returns name, value, convention
              name, value, _ = winreg.EnumValue(key, i)
              autostarts.append((name, value))
              i += 1
          except OSError:
              break

      return autostarts
    
    def get_startupfolder_autostarts(self):
        startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

        autostarts = []

        for item in os.listdir(startup_folder):
            item_path = os.path.join(startup_folder, item)
            if os.path.isfile(item_path):
                autostarts.append({ 
                      'name': item, 
                      'path': item_path 
                     }
                )

        return autostarts


    
