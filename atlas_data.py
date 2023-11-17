import pymongo
import sys
from getpass import getpass
import json
import os
from get_data import get_choice
from urllib.parse import quote
from config import *

### CLASS DEFINITIONS ###
class DBHandler:
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
        try: 
            result=self.collection.insert_many(self.jsons)
        # return a friendly error if the operation fails
        except pymongo.errors.OperationFailure as e:
            print("Operation error. Are you authorized to upload data?")
            print(str(e))
            return 0
        
        inserted_count=len(result.inserted_ids)
        print(f"Successfully uploaded {inserted_count} file{'s' if inserted_count>1 else ''}.")
        
        return 1
    
    def download(self, search_result):
        # Given some search result, download that data from database.
        pass
    
    def search(self, query=None):
        # Given some query, find data that matches that description.
        result=self.collection.find(query)

        if result:    
            for doc in result:
                my_recipe=doc['name']
                my_ingredient_count=len(doc['ingredients'])
                my_prep_time=doc['prep_time']
                print("%s has %x ingredients and takes %x minutes to make." %(my_recipe, my_ingredient_count, my_prep_time))
                
        else:
            return None

### BEGIN MAIN ###
if __name__=="__main__":
    ''' TODO:
    * See https://www.mongodb.com/docs/manual/tutorial/update-documents/ for help

    * Index in database based either on custom hash ID, or remove it and just index based
      on both the writer ID and the prompt using MongoDB special indexing.

    * For repeated prompts (for analyzing how handwriting changes), just allow duplicate
      indices in the database. The save_time_date will serve as differentiation during analysis.

    '''

    data=DBHandler()
    print("Successfully connected to database.")
    action=get_choice("Uploading or downloading (and searching for) data?\n1. Uploading\n2. Downloading\n", "1", "2")

    if action=='1': # Uploading data
        # Currently, default location is only data upload location.
        data.load_local_jsons()
        if data.upload():
            print("Upload successful.")
        else:
            print("Upload failed.")
    else: # Downloading data
        print("Not yet implemented")
        sys.exit(1)
        # Allow user to search for data
        search_query=None # Some object?
        search_result=data.search(search_query) # A dataset that matches query.
        if search_result:
            data.download(search_result)

    sys.exit(1)
    '''
    handwriting_data=data.db["handwriting_data"]

    if action=="a":
        upload_data(db)
    else:


    fnames=[]
    for dirpath, dirnames, filenames in os.walk(DATA_PATH):
        if dirnames:
            continue
        for filename in filenames:
            if filename.startswith('.'):
                continue
            fnames.append(os.path.join(dirpath, filename))

    json_files=[]
    for fname in fnames:
        with open(fname) as f:
            json_files.append(json.load(f))

    print(json_files)
    input("Worked. Exit now.")

    try:
        for json_data in json_files:
            result=handwriting_data.insert_many(json_data)

    # return a friendly error if the operation fails
    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
    else:
        inserted_count=len(result.inserted_ids)
        print("I inserted %x documents." %(inserted_count))

        print("\n")



# use a database named "myDatabase"
db=client.myDatabase

# use a collection named "recipes"
my_collection=db["recipes"]

recipe_documents=[{ "name": "elotes", "ingredients": ["corn", "mayonnaise", "cotija cheese", "sour cream", "lime"], "prep_time": 35 },
                    { "name": "loco moco", "ingredients": ["ground beef", "butter", "onion", "egg", "bread bun", "mushrooms"], "prep_time": 54 },
                    { "name": "patatas bravas", "ingredients": ["potato", "tomato", "olive oil", "onion", "garlic", "paprika"], "prep_time": 80 },
                    { "name": "fried rice", "ingredients": ["rice", "soy sauce", "egg", "onion", "pea", "carrot", "sesame oil"], "prep_time": 40 }]

# drop the collection in case it already exists
try:
  my_collection.drop()  

# return a friendly error if an authentication error is thrown
except pymongo.errors.OperationFailure:
  print("An authentication error was received. Are your username and password correct in your connection string?")
  sys.exit(1)

# INSERT DOCUMENTS
#
# You can insert individual documents using collection.insert_one().
# In this example, we're going to create four documents and then 
# insert them all with insert_many().

try: 
 result=my_collection.insert_many(recipe_documents)

# return a friendly error if the operation fails
except pymongo.errors.OperationFailure:
  print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
  sys.exit(1)
else:
  inserted_count=len(result.inserted_ids)
  print("I inserted %x documents." %(inserted_count))

  print("\n")

# FIND DOCUMENTS
#
# Now that we have data in Atlas, we can read it. To retrieve all of
# the data in a collection, we call find() with an empty filter. 

result=my_collection.find()

if result:    
  for doc in result:
    my_recipe=doc['name']
    my_ingredient_count=len(doc['ingredients'])
    my_prep_time=doc['prep_time']
    print("%s has %x ingredients and takes %x minutes to make." %(my_recipe, my_ingredient_count, my_prep_time))
    
else:
  print("No documents found.")

print("\n")

# We can also find a single document. Let's find a document
# that has the string "potato" in the ingredients list.
my_doc=my_collection.find_one({"ingredients": "potato"})

if my_doc is not None:
  print("A recipe which uses potato:")
  print(my_doc)
else:
  print("I didn't find any recipes that contain 'potato' as an ingredient.")
print("\n")

# UPDATE A DOCUMENT
#
# You can update a single document or multiple documents in a single call.
# 
# Here we update the prep_time value on the document we just found.
#
# Note the 'new=True' option: if omitted, find_one_and_update returns the
# original document instead of the updated one.

my_doc=my_collection.find_one_and_update({"ingredients": "potato"}, {"$set": { "prep_time": 72 }}, new=True)
if my_doc is not None:
  print("Here's the updated recipe:")
  print(my_doc)
else:
  print("I didn't find any recipes that contain 'potato' as an ingredient.")
print("\n")

# DELETE DOCUMENTS
#
# As with other CRUD methods, you can delete a single document 
# or all documents that match a specified filter. To delete all 
# of the documents in a collection, pass an empty filter to 
# the delete_many() method. In this example, we'll delete two of 
# the recipes.
#
# The query filter passed to delete_many uses $or to look for documents
# in which the "name" field is either "elotes" or "fried rice".

my_result=my_collection.delete_many({ "$or": [{ "name": "elotes" }, { "name": "fried rice" }]})
print("I deleted %x records." %(my_result.deleted_count))
print("\n")
'''