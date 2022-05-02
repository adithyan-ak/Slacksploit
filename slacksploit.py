import os, sys, time
import platform, getpass
import csv
import ccl_leveldb
import pathlib

banner = '''
  _____ _            _              _       _ _   
 / ____| |          | |            | |     (_) |  
| (___ | | __ _  ___| | _____ _ __ | | ___  _| |_ 
 \___ \| |/ _` |/ __| |/ / __| '_ \| |/ _ \| | __|
 ____) | | (_| | (__|   <\__ \ |_) | | (_) | | |_ 
|_____/|_|\__,_|\___|_|\_\___/ .__/|_|\___/|_|\__|
                             | |                  
                             |_|                  
'''
ENCODING = "iso-8859-1" # Encoding for parsing and dumping the leveldb contents into CSV

def checklocation(path):
    return os.path.isdir(path)

def typingPrint(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)

def dumb_leveldb(input_path):
    output_path = input_path.split("/")[-2] + "dump.csv"

    print("Parsing the leveldb files from "+input_path)

    leveldb_records = ccl_leveldb.RawLevelDb(input_path)

    with open(output_path, "w", encoding="utf-8", newline="") as file1:
        writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
        writes.writerow(
            [
                "key-hex", "key-text", "value-hex", "value-text", "origin_file",
                "file_type", "offset", "seq", "state", "was_compressed"
            ])

        for record in leveldb_records.iterate_records_raw():
            writes.writerow([
                record.user_key.hex(" ", 1),
                record.user_key.decode(ENCODING, "replace"),
                record.value.hex(" ", 1),
                record.value.decode(ENCODING, "replace"),
                str(record.origin_file),
                record.file_type.name,
                record.offset,
                record.seq,
                record.state.name,
                record.was_compressed
            ])
    print("The leveldb content has been written into "+output_path)


if __name__ == '__main__':

    print(banner)

    opsys = platform.system()
    opsysversion = platform.release()
    hostname = platform.node()
    user = getpass.getuser()

    print("OS : "+opsys)
    print("System Version : "+opsysversion)
    print("Hostname : "+hostname)
    print("User : "+user)

    mac_slack_resource = "/Applications/Slack.app/Contents/Resources/"
    mac_slack_storage = "/Users/adithyanak/Library/Application Support/Slack/"
    wins_slack_resource = "C:/Users/" + "username" + "/AppData/Local/slack/"
    wins_slack_storage = "C:/Users/" + "username" + "/AppData/Roaming/Slack/"
    linux_slack_resource = "~/snap/slack/60/etc/"
    linux_slack_storage = "~/snap/slack/60/.config/Slack/"

    print("Enumerating OS for Slack Installation ....")

    leveldb_locations = []

    if opsys == "Darwin":
        if checklocation(mac_slack_storage):
            print("Found Slack Storage Directory: "+mac_slack_storage)
        if checklocation(mac_slack_resource):
            print("Found Slack Storage Directory: "+mac_slack_resource)
        if checklocation(mac_slack_storage+"Session Storage/"):
            leveldb_locations.append(mac_slack_storage+"Session Storage/")
        if checklocation(mac_slack_storage+"/IndexedDB/https_app.slack.com_0.indexeddb.leveldb/"):
            leveldb_locations.append(mac_slack_storage+"/IndexedDB/https_app.slack.com_0.indexeddb.leveldb/")
        if checklocation(mac_slack_storage+"/Local Storage/leveldb/"):
            leveldb_locations.append(mac_slack_storage+"/Local Storage/leveldb/")
        

    elif opsys == "Windows":
        if checklocation(wins_slack_storage):
            print("Found Slack Storage Directory: "+wins_slack_storage)
        if checklocation(wins_slack_resource):
            print("Found Slack Storage Directory: "+wins_slack_resource)

    elif opsys == "Linux":
        if checklocation(linux_slack_storage):
            print("Found Slack Storage Directory: "+linux_slack_storage)
        if checklocation(linux_slack_resource):
            print("Found Slack Storage Directory: "+linux_slack_resource)

    else:
        print("Slacksploit isn't supported for the given Operating system")
        quit()

    print("Examining LevelDB Files")

    for loc in leveldb_locations:
        dumb_leveldb(loc)
