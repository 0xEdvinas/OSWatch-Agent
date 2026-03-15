import collectors.autostarts.autostarts_collector as autostarts_collector

def main():
   collector = autostarts_collector.AutostartsCollector()

   autostarts = collector.get_startupfolder_autostarts()

   for autostart in autostarts:
         print(f"Name: {autostart['name']}, Path: {autostart['path']}")

if __name__ == "__main__":    
   main()