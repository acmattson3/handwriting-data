# handwriting-data
A way to gather and provision handwriting data, as well as some ways to use handwriting data (handwriting synthesis, copying (GCODE), and displaying (SVG))

## How to Use

### Data Creation
You will need Python 3 to run this project. You can install it on Linux using ```sudo apt-get install python3 -y```. You will also want pip; install it with ```sudo apt-get install python3-pip```

Then, you will need to install the libraries required to run this project. You can do this using ```pip install -r requirements.txt```. 

Before you run the drawing software, you should modify the config.py file. The first two constants are set to a value of -1 and -1,-1. Please set these values as specified in the config.py file (the height of your screen and your screen's resolution). For example, my constants in the config file look like this:
```python3
''' config for handwriting-data
* Contains user dependent constants
* Contains other configurable program settings
'''

# by default, screen height is -1, and resolution is -1,-1. Please change these values.

### USER CONFIGURED CONSTANTS ###
# Used to calculate pixels per millimeter value.
SCREEN_HEIGHT=200 # The height of your screen, in millimeters.
SCREEN_RES_X,SCREEN_RES_Y=1920,1080 # The resolution of your screen (ex., 1920x1080 becomes 1920,1080)

...
```
Once you get the program running, you will be prompted to enter some user information and configurations. First, enter your desired writer ID (usually your name). You will be asked to confirm your name was received correctly.

Next, specify whether you want to use prompts or not. Prompt mode generates the JSON files based on the prompt displayed for you. Non-prompt mode is used for generating SVG and GCODE files.

In prompt mode, you are asked to enter any other user data you wish to collect. If you wish to enter other user data, you will be asked for a "category name" which is the key in the JSON file. You will then be asked to enter the data value for that category. You may add as much other user data as desired. 

In non-prompt mode, you will be asked to specify the size of your window in either pixels or millimeters. 

Once you make it through the configurations, the drawing window will open up. In prompt mode, the prompt window will open up as well. Now, you may draw in the drawing window. Press S to generate an SVG file of the your current window, G to generate GCODE based on your current window, and (in prompt mode only) ENTER to submit your current window and generate a JSON file. Press Z to clear the current window, and ESC to exit.

### Data Uploading/Downloading
To upload or download data, you will need access to the MongoDB Atlas database created for this project. The public account uses this connection string: ```mongodb+srv://public:GimmeWritingData@HandwritingData.lbgarej.mongodb.net/```. As such, the username is ```public``` and the password is ```GimmeHandwritingData```. Use MongoDB's Compass to download data using this account. To upload data, you will need authorization by a developer. You should use ```atlas_data.py``` to upload prompt data (it will ask you for an authorized username and password).

## Overall Project Architecture
Below is a diagram showing the overall project architecture.
![image](https://github.com/acmattson3/handwriting-data/assets/112522139/45a2479d-d28f-4edd-90dd-ecdbc34d9813)


## Creating Data (complete)
The data gathering portion involves a basic OpenCV drawing program used to collect pixel data of a user's pen strokes as they write. To use it, launch main.py using ```python3 main.py```. 

The program begins by asking for the user's name. It then asks the user how they want to use the program (prompt-mode for generating JSON data, and non-prompt-mode for generating SVG's or GCODE). Then, the interactive writing program launches. In prompt mode, the text window provides the user with a prompt. The user writes this prompt using a digital tablet (such as a [Gaomon Tablet](https://gaomon.net/)), writing within the drawing window. The program logs the writing, recording each pen stroke in the form of a JSON file. This is how the handwriting data is created. In non-prompt mode, the user can draw freely in a window of their chosen size and save that data as an SVG or GCODE file. 

## Storing Data (complete)
After the user completes a prompt (prompt-mode) or writes something custom (non-prompt-mode), that data can be stored in a few different ways (as previously stated):
1. A GCODE file format, given a user's screen's pixel/mm ratio (by pressing 'g' on the keyboard)
2. An SVG file format (by pressing 's' on the keyboard)
3. A JSON file format (by pressing 'enter' on the keyboard) (prompt-mode only)

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

**If you are interested in synthesizing your own handwriting using AI, please read** [**the README in the prompts directory**](https://github.com/acmattson3/handwriting-data/tree/main/prompts#preparing-data). There, I walk through the steps of training the [previously mentioned handwriting synthesis AI](https://github.com/sjvasquez/handwriting-synthesis) on your own handwriting data generated by my drawing program. 

## Accessibility and Provisioning (complete, with future revisions/additions likely)
To increase its accessibility, handwriting data will be uploaded to an online database hosted on the cloud. I am using MongoDB's Atlas cloud database due to its intuitive API's and premade graphical user interfaces. This will allow anyone to upload (with proper authentication) or download handwriting data as desired. MongoDB allows data to be accessed through indexing, allowing users to retrieve exactly the data they need. Until this point, everything has been part of the same program, as data creation and storage are part of data "gathering." This next part, data provisioning, is a separate program that works alongside this one to take this gathered data and upload it to the database (called atlas_data.py). There is also a program created by MongoDB called Compass that makes for an easy way to search for and download data.

**How to access the handwriting database:**
* [**MongoDB Compass**](https://www.mongodb.com/try/download/compass) **for downloading** - MongoDB's Compass is a program built by MongoDB with an intuitive graphical user interface.
  * It connects to the database using a "connection string" for the database.
  * The connection string for the handwriting database is
    ```mongodb+srv://<username>:<password>@HandwritingData.lbgarej.mongodb.net/```.
* **atlas_data.py for uploading** - A specially-written terminal-based program.
  * Incorporates the connection string in code so you don't have to (prompts you for a username and password on startup).
  * Integrates seamlessly with the JSON drawing software to upload locally generated data in one step.

**I highly recommend that anyone uploading locally generated data use atlas_data.py rather than MongoDB's Compass.** Downloading and searching for data is only possible through MongoDB's Compass. I did try to integrate data searching and downloading in atlas_data.py, but my results were terrible compared to the ease of use that Compass provides.

The public, download-only, account for this data on the database is:
* **Username:** public
* **Password:** GimmeWritingData

So, the connection string is ```mongodb+srv://public:GimmeWritingData@HandwritingData.lbgarej.mongodb.net/```.

If you wish to upload data, please contact me.
