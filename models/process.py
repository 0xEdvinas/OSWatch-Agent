class Process:
  name: str
  path: str
  startup_status: str

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