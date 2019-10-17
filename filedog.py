import os



def main():
    FILEDOG_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    FILEDOG_DATA_DIR = f"{FILEDOG_BASE_DIR}\\filedog_settings"
    FILEDOG_TARGETLIST_JSON = f"{FILEDOG_DATA_DIR}\\targets.json"

    if not os.path.exists(FILEDOG_DATA_DIR):
        os.makedirs(FILEDOG_DATA_DIR)
    if not os.path.exists(FILEDOG_TARGETLIST_JSON):
        with open(FILEDOG_TARGETLIST_JSON, "w") as targetfile:
            targetfile.writelines(["[\n","\t\n","]"])
        print("Created missing target file, need to populate with paths to watch.")
        print(f"File located at: '{FILEDOG_TARGETLIST_JSON}'", end="\n\n")
        return None

    return None

if __name__ == "__main__":
    main()