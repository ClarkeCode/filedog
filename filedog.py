import os

id_value_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
def generateID(someIntVal: int) -> str:
    """Takes an integer number and creates a 5-digit alphanumeric id"""
    id_offsets = []
    for exp in range(5,0,-1):
        div = len(id_value_index) ** exp
        id_offsets.append(int(someIntVal/div))
        someIntVal = someIntVal % div
        if (exp == 1):
            id_offsets.append(someIntVal)
    
    generated_id = ""
    for x in id_offsets:
        generated_id += id_value_index[x]
    return generated_id

FILEDOG_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
INCREMENT_NUMBER = 0
def write_number_to_file(filePath: str, number: int) -> None:
    with open(filePath, "w") as targetfile:
        targetfile.write(str(number))

def on_created(event):
    print(f"{event.src_path}' has been created!")
    
    file_path, file_extension = os.path.splitext(event.src_path)
    file_path, file_name = file_path.rsplit("\\", 1)
    print((file_path, file_name, file_extension))

    #TODO: make this behaviour trigger if a match is found in a regex file
    if file_name == "image0":
        try:
            global INCREMENT_NUMBER
            new_id = generateID(INCREMENT_NUMBER)
            INCREMENT_NUMBER += 1
            os.rename(event.src_path, f"{file_path}\\{new_id}{file_extension}")
        except FileExistsError:
            print("Already exists")
    print()


def main():
    FILEDOG_DATA_DIR = f"{FILEDOG_BASE_DIR}\\filedog_settings"
    FILEDOG_TARGETLIST_JSON = f"{FILEDOG_DATA_DIR}\\targets.json"
    FILEDOG_INCREMENT_FILE = f"{FILEDOG_DATA_DIR}\\id_offset.txt"
    
    print("Starting filedog...")
    if not os.path.exists(FILEDOG_DATA_DIR):
        os.makedirs(FILEDOG_DATA_DIR)

    if not os.path.exists(FILEDOG_INCREMENT_FILE):
        write_number_to_file(FILEDOG_INCREMENT_FILE, 0)
        INCREMENT_NUMBER = 0
    else:
        with open(FILEDOG_INCREMENT_FILE, "r") as targetfile:
            INCREMENT_NUMBER = int(targetfile.readline())

    #Loading info from JSON setting files
    #####################################
    import json
    def displayFriendlyJSONErr(jsonError: json.decoder.JSONDecodeError):
        print(f"Encountered a JSON parsing error for targets.json")
        print(f"Malformed line is at line {jsonError.lineno}, column {jsonError.colno}: '{jsonError.msg}'")
        print(f"\nCheck for errors at '{FILEDOG_TARGETLIST_JSON}'")
        print("\nStopping filedog...")

    PATHS_TO_MONITOR = []
    if not os.path.exists(FILEDOG_TARGETLIST_JSON):
        with open(FILEDOG_TARGETLIST_JSON, "w") as targetfile:
            targetfile.writelines(["[\n", "\t\"" + FILEDOG_BASE_DIR.replace("\\","\\\\") +"\"\n", "]"])
        print("Created missing target file, need to populate with paths to watch.")
        print(f"File located at: '{FILEDOG_TARGETLIST_JSON}'", end="\n\n")
        return None
    else:
        try:
            PATHS_TO_MONITOR = json.load(open(FILEDOG_TARGETLIST_JSON))
        except json.decoder.JSONDecodeError as err:
            displayFriendlyJSONErr(err)
            return None

    #TODO: load list of regexes to trigger renaming


    from watchdog.events import RegexMatchingEventHandler
    patterns = [r".*"]
    ignore_patterns = [""]
    ignore_directories = True
    case_sensitive = False
    my_event_handler = RegexMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created #TODO: make custom handler more obvious
    
    from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
    go_recursively = True

    OBSERVER_LIST = []
    for path in PATHS_TO_MONITOR:
        filesys_observer = Observer()
        filesys_observer.schedule(my_event_handler, path, recursive=go_recursively)
        OBSERVER_LIST.append(filesys_observer)
    
    for ob in OBSERVER_LIST:
        ob.start()


    #Main thread waits until finished
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        for ob in OBSERVER_LIST:
            ob.stop()
            ob.join()
        #do other cleanup behaviours
        print("Stopping filedog...")
    return None

if __name__ == "__main__":
    main()