class Process:
  name: str
  path: str
  # !!! WINDOWS-SPECIFIC BEHAVIOR !!!
  # If app is in: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
  # But not in: HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run
  # then we assume it's enabled, since the latter key is where Windows stores the enabled/disabled status of autostarts
  startup_status: str = "enabled"

  def __init__(self, name: str, path: str):
    self.name = name
    self.path = path

  def set_startup_status(self, status: str):
    self.startup_status = status

  def get_name(self) -> str:
    return self.name
  
  def get_path(self) -> str:
    return self.path
  
  def get_status(self) -> str:
    return self.startup_status
  

  # TODO: rename to autostart_info or something, since this is not a general process model but specific to autostarts