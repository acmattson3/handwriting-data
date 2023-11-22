# handwriting-data
A way to gather and provision handwriting data.

## Creating Data (complete)
The data gathering portion involves a basic OpenCV drawing program used to collect pixel data of a user's pen strokes as they write. 

The program begins by asking for the user's information, including their name and general location. The program also automatically gathers the start/end time, program version, and drawing window size. Then, the interactive writing program launches. The text window provides the user with a prompt. The user writes this prompt using a digital tablet (such as a [Gaomon Tablet](https://gaomon.net/)), writing within the drawing window. As the user writes, the program records the resulting cursor events (mouse up/down) and movement data (x/y coordinates and timing) in memory.

## Storing Data (complete)
After the user completes a prompt or writes something custom, that data can be stored in a few different ways:
1. A GCODE file format, given a user's screen's pixel/mm ratio (by pressing 'g' on the keyboard)
2. An SVG file format (by pressing 's' on the keyboard)
3. A JSON file format (by pressing 'enter' on the keyboard)

### GCODE Format (complete)
Converting the writing data to GCODE exactly copies the user's input data, millimeter by millimeter, into GCODE. This allows users with a CNC writing robot (or modified 3D printer, like me) to repeatedly and exactly copy their own or somebody else's handwriting. There are many applications for this file format, such as:
* Mass-producing personalized letters (ex., handwritten invitations, thank you cards, etc.), where only a few components change from letter-to-letter (i.e., the recipient's name, which the user can write in manually).
* Replicating a signature without need for the signer's presence (so long as the GCODE is intentionally used and validated by the signer or an authorized representative appointed by the signer).

### SVG Format (complete)
SVG files are primarily used for graphics, and are an extremely lightweight file format. From my research, no program exists with the sole purpose of converting a hand-made drawing or handwriting into an SVG file format. With an SVG handwriting or drawing file, someone can:
* Display that handwriting or drawing on a webpage
  * The extremely light file size allows for high webpage responsiveness.
  * Great for displaying generally hard-to-digitize information, such as complex math or drawings.
* Create an easily-transferrable digital signature (so long as the SVG file is intentionally used and validated by the signer or an authorized representative appointed by the signer) for signing digital documents.

### XML Format (DISCONTINUED)
The XML format was found to be much more complicated than was necessary. JSON will be used instead.

### JSON Format (complete)
Storing the handwriting data in a JSON format gives a vast array of information that is easily parsable. The JSON files include the time taken for each stroke, as well as the writer's location, name, and (optionally) other user data like age or finger-length, making it highly valuable for statistical analysis and answering questions like: 
* Does finger length correlate with writing speed? 
* What combinations of letters take the longest to write? 
* Are certain writing styles faster than others?
* How does an elementary school student's handwriting improve over time? How, fundamentally, is it improving? Are they writing faster? More legibly? Both? What letters take the longest to improve on?

Another use, and the one I am most interested in, is using this JSON format to train an AI model, [like this one](https://github.com/sjvasquez/handwriting-synthesis), to allow the model to replicate your handwriting. The uses for this are vast, including, but not limited to:
* Fully AI-generated (including what is being written) hyper-realistic writing
* Mass producing personalized handwritten letters (via AI or auto-fill scripts) with no need for user intervention
* A step-by-step, fully-automated, browser-based AI writing instructor for teaching people of all ages how to write in new styles or foreign languages.
* An automatic handwriting transcription software

## Accessibility and Provisioning (in progress)
To increase its accessibility, handwriting data will be uploaded to an online database hosted on the cloud. I am using MongoDB's Atlas cloud database due to its intuitive API's and premade graphical user interfaces. This will allow anyone to upload (with proper authentication) or download handwriting data as desired. MongoDB allows data to be accessed through indexing, allowing users to retrieve exactly the data they need. Until this point, everything has been part of the same program, as data creation and storage are part of data "gathering." This next part, data provisioning, will be a separate program that works alongside this one to take this gathered data and upload it to the database. 

**There are two recommended ways to access the handwriting data:**
* [**MongoDB Compass**](https://www.mongodb.com/try/download/compass) - MongoDB's Compass is a program built by MongoDB with an intuitive graphical user interface.
  * It connects to the database using a "connection string" for the database.
  * The connection string for my database is
    ```mongodb+srv://<username>:<password>@HandwritingData.lbgarej.mongodb.net/```.
* **atlas_data.py** - A terminal-based program written by yours truly.
  * Incorporates the connection string in code so you don't have to (prompts you for a username and password on startup).
  * Integrates seamlessly with my JSON drawing software. Upload your data in one easy step!
  * The hard part about my program is creating some easy way for users to search for data; a GUI, like seen with Compass, is best for searching for and downloading data.

**I highly recommend that anyone accessing my data use the MongoDB Compass interface for searching for and downloading data, and my program for uploading data.**

The public, download-only, account for this data on the database is:
* **Username:** public
* **Password:** GimmeWritingData

So, the connection string is ```mongodb+srv://public:GimmeWritingData@HandwritingData.lbgarej.mongodb.net/```.
