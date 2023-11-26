import pymongo
import sys
from getpass import getpass
import json
import os
from get_data import get_choice
from urllib.parse import quote
from config import *

### CLASS DEFINITION ###
class DBHandler: # For dealing with Atlas handwriting database
    def __init__(self):
        print("Attempting to access database. Please enter your credentials.")
        self.username=str(input("Username: "))

        # Deal with password
        password=str(getpass())

        self.connection_string=f"mongodb+srv://{quote(self.username)}:{quote(password)}@{quote(DATABASE_NAME)}.lbgarej.mongodb.net/?retryWrites=true&w=majority"
        try:
            self.client=pymongo.MongoClient(self.connection_string)
        except pymongo.errors.ConfigurationError:
            print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
            sys.exit(1)
        
        self.db=self.client.HandwritingData
        self.jsons=[]
        self.collection=self.db["handwriting"]
        self.loaded_file_num=0

    # Get json files from local DATA_PATH directory.
    def load_local_jsons(self):
        self.jsons=[]
        fnames=[]
        for dirpath, dirnames, filenames in os.walk(PROMPT_DATA_DIR):
            if dirnames:
                continue
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                fnames.append(os.path.join(dirpath, filename))

        self.loaded_file_num=0
        for fname in fnames:
            if ".json" in fname:
                with open(fname) as f:
                    self.jsons.append(json.load(f))
                self.loaded_file_num+=1

    def upload(self):
        if self.loaded_file_num<1:
            print("No data loaded.")
            return 0
        print("Attempting to upload data...")

        inserted_count=0
        try: # Upload the data
            result=self.collection.insert_many(self.jsons)
        # return a friendly error if the operation fails
        except pymongo.errors.OperationFailure as e:
            print("Operation error. Are you authorized to upload data?")
            print(str(e))
            return 0
        
        inserted_count=len(result.inserted_ids)
        print(f"Successfully uploaded {inserted_count} file{'s' if inserted_count>1 else ''}.")
        
        return 1


### BEGIN MAIN ###
if __name__=="__main__":
    data=DBHandler()
    print("Successfully connected to database.")
    action=get_choice("You are attempting to upload your local data. Would you like to continue?", "y", "n")

    if action=='y': # Uploading data
        # Currently, default location is only data upload location.
        data.load_local_jsons() # Load local data
        if data.upload(): # Upload the loaded data
            print("Upload successful.")
        else:
            print("Upload failed.")