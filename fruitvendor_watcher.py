#fruitpal file watchdog and JSON translator

"""
This file runs in the baxkground once started and waits for the JSON text
file to change. Once it has detected a change it parses the JSON and 
translates it into a python dict that is available for import by the 
fruitpal_cli file.
"""
import json
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 

import os
import time

FRUIT_DICT = {}

def getJson()->dict:
    cwd = os.getcwd()

    fruit_pal_dict = { "COUNTRIES": set(), "FRUITS": set() }


    with open(cwd+"/Data/fruit_data.txt") as fruit_data:
        data = json.load(fruit_data)
        for entry in data:
            country = entry["COUNTRY"]
            fruit = entry["COMMODITY"]
            for k,v in entry.items():
                if k not in ["COUNTRY","COMMODITY"]:
                    fruit_pal_dict.setdefault(fruit, {}).setdefault(country,{})[k] = v

            fruit_pal_dict["COUNTRIES"].add(country)
            fruit_pal_dict["FRUITS"].add(fruit)
    return fruit_pal_dict



class MyWatcher(PatternMatchingEventHandler):
    """
    This class is based on the PatternMatchingEventHandler class from watchdog.
    This class looks for files in a specific dir that match the pattern when a
    new one is created or a current one is modified.
    """
    pattern=["*.txt"]


    def parse_json_on_event(self, event)->None:
        """
        This function runs when the watcher detects a file event. The event 
        created by the watchdog.events module has three relevant properties:

            event.event_type
                'modified' | 'created'
            event.is_directory
                True | False
            event.src_path
                path/to/observed/file


        """

        # Open the flat file fruit_data.txt from the Data/ directory
        print("parsing JSON!!")
        FRUIT_DICT = getJson()
        print("finished parsing JSON!!")
        print(FRUIT_DICT)
            


    def on_modified(self, event):
        """
        Override method of PatternMatchingEventHandler that is called when a
        file is modified
        """
        print("fruitpal data has been modified")
        self.parse_json_on_event(event)
        print(FRUIT_DICT)

    def on_created(self, event):
        """
        Override method of PatternMatchingEventHandler that is called when a
        file is created
        """
        self.parse_json_on_event(event)

def Main():
    cwd = os.getcwd()
    path = cwd + "/Data"
    observer = Observer()
    observer.schedule(MyWatcher(), path=path)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    Main()

  