import subprocess
import winreg
import os
import models.process as process

class AutostartsCollector:  
    
import winreg
import process


class AutostartsCollector:
    def get_registry_autostarts(self) -> list[process.Process]:
        path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)

        i = 0
        autostarts: list[process.Process] = []

        while True:
            try:
                # returns: name, value, type
                name, path_value, _ = winreg.EnumValue(key, i)
                autostarts.append(process.Process(name, path_value))
                i += 1
            except OSError:
                break

        return autostarts

    def get_registry_autostart_statuses(self) -> dict[str, str]:
        path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)

        i = 0
        statuses: dict[str, str] = {}

        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)

                # value is bytes because this key uses REG_BINARY
                first_byte = value[0] if value else None

                if first_byte == 2:
                    status = "enabled"
                elif first_byte == 3:
                    status = "disabled"
                else:
                    status = "unknown"

                statuses[name] = status
                i += 1
            except OSError:
                break

        return statuses

    def get_registry_autostarts_with_status(self) -> list[process.Process]:
        autostarts = self.get_registry_autostarts()
        statuses = self.get_registry_autostart_statuses()

        for app in autostarts:
            status = statuses.get(app.get_name(), "enabled")
            app.set_startup_status(status)

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
    
    def get_scheduled_tasks_autostarts(self):
        result = subprocess.run(['schtasks', '/query', '/fo', 'LIST'], capture_output=True, text=True)
        output = result.stdout

        autostarts = []
        current_task = {}

        for line in output.splitlines():
            if line.startswith("TaskName:"):
                if current_task:
                    autostarts.append(current_task)
                    current_task = {}
                current_task['name'] = line.split(":", 1)[1].strip()
            elif line.startswith("Task To Run:"):
                current_task['path'] = line.split(":", 1)[1].strip()

        if current_task:
            autostarts.append(current_task)

        return autostarts
    
    def get_windows_services_autostarts(self):
        result = subprocess.run(['sc', 'query', 'state=all'], capture_output=True, text=True)
        output = result.stdout

        autostarts = []
        current_service = {}

        for line in output.splitlines():
            if line.startswith("SERVICE_NAME:"):
                if current_service:
                    autostarts.append(current_service)
                    current_service = {}
                current_service['name'] = line.split(":", 1)[1].strip()
            elif line.startswith("BINARY_PATH_NAME:"):
                current_service['path'] = line.split(":", 1)[1].strip()

        if current_service:
            autostarts.append(current_service)

        return autostarts