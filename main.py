import collectors.autostarts.autostarts_collector as autostarts_collector

def main():
   collector = autostarts_collector.AutostartsCollector()

   autostarts = collector.get_registry_autostarts()

   for autostart in autostarts:
      print(f"Name: {autostart.get_name()}, Path: {autostart.get_path()}")

if __name__ == "__main__":    
   main()