import os

id_value_index = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
def generateID(someIntVal: int) -> str:
    """Takes an integer number and creates a 5-digit alphanumeric id"""
    id_offsets = []
    for exp in range(4,0,-1):
        div = len(id_value_index) ** exp
        id_offsets.append(int(someIntVal/div))
        someIntVal = someIntVal % div
        if (exp == 1):
            id_offsets.append(someIntVal)
    
    generated_id = ""
    for x in id_offsets:
        generated_id += id_value_index[x]
    return generated_id

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