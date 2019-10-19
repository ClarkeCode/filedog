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

    if file_name == "image0":
        try:
            global INCREMENT_NUMBER
            new_id = generateID(INCREMENT_NUMBER)
            INCREMENT_NUMBER += 1
            os.rename(event.src_path, f"{file_path}\\{new_id}{file_extension}")
        except FileExistsError:
            print("Already exists")
    print()

#def on_deleted(event):
#    print(f"'{event.src_path}' was deleted!")
#def on_modified(event):
#    print(f"'{event.src_path}' has been modified")
#def on_moved(event):
#    print(f"'{event.src_path}' was moved to '{event.dest_path}'")

def main():
    FILEDOG_DATA_DIR = f"{FILEDOG_BASE_DIR}\\filedog_settings"
    FILEDOG_TARGETLIST_JSON = f"{FILEDOG_DATA_DIR}\\targets.json"
    FILEDOG_INCREMENT_FILE = f"{FILEDOG_DATA_DIR}\\id_offset.txt"

    if not os.path.exists(FILEDOG_DATA_DIR):
        os.makedirs(FILEDOG_DATA_DIR)

    if not os.path.exists(FILEDOG_INCREMENT_FILE):
        write_number_to_file(FILEDOG_INCREMENT_FILE, 0)
        INCREMENT_NUMBER = 0
    else:
        with open(FILEDOG_INCREMENT_FILE, "r") as targetfile:
            INCREMENT_NUMBER = int(targetfile.readline())

    PATHS_TO_MONITOR = []
    if not os.path.exists(FILEDOG_TARGETLIST_JSON):
        with open(FILEDOG_TARGETLIST_JSON, "w") as targetfile:
            targetfile.writelines(["[\n", f"\t{FILEDOG_BASE_DIR}\n", "]"])
        print("Created missing target file, need to populate with paths to watch.")
        print(f"File located at: '{FILEDOG_TARGETLIST_JSON}'", end="\n\n")
        return None
    else:
        import json
        PATHS_TO_MONITOR = json.load(open(FILEDOG_TARGETLIST_JSON))


    from watchdog.events import RegexMatchingEventHandler
    patterns = [r".*"]
    ignore_patterns = [""]
    ignore_directories = False
    case_sensitive = False
    my_event_handler = RegexMatchingEventHandler(ignore_directories=True)#patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    #my_event_handler.on_deleted = on_deleted
    #my_event_handler.on_modified = on_modified
    #my_event_handler.on_moved = on_moved
    
    
    #from watchdog.observers import Observer
    from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
    #path = "."
    go_recursively = True
    #my_observer = Observer()
    #my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    OBSERVER_LIST = []
    for path in PATHS_TO_MONITOR:
        filesys_observer = Observer()
        filesys_observer.schedule(my_event_handler, path, recursive=go_recursively)
        OBSERVER_LIST.append(filesys_observer)
    
    for ob in OBSERVER_LIST:
        ob.start()

    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for ob in OBSERVER_LIST:
            ob.stop()
            ob.join()
        #do other cleanup behaviours
    return None

if __name__ == "__main__":
    main()