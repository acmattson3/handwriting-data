# handwriting-data
A way to gather, store, and retrieve handwriting data.

## Gathering Data (complete)
The data gathering portion involves a basic OpenCV drawing program used to collect pixel data of a user's pen strokes as they write. 

The program begins by asking for the user's information, including their name and general location. The program also automatically gathers the start/end time, program version, and drawing window size. Then, the interactive writing program launches. The text window provides the user with a prompt. The user writes this prompt using a digital tablet (such as a [Gaomon Tablet](https://gaomon.net/)), writing within the drawing window. As the user writes, the program records the resulting cursor events (mouse up/down) and movement data (x/y coordinates and timing) in memory.

## Storing Data (in progress)
After the user completes a prompt or writes something custom, that data can be stored in a few different ways:
1. A GCODE file format, given a user's screen's pixel/mm ratio (by pressing 'g' on the keyboard)
2. An XML file format, as seen [here](https://fki.tic.heia-fr.ch/static/iamondb/strokesz.xml) (by pressing 'enter' on the keyboard)
3. An SVG file format (by pressing 's' on the keyboard)

### GCODE Format (complete)
Converting the writing data to GCODE exactly copies the user's input data, millimeter by millimeter, into GCODE. This allows users with a CNC writing robot (or modified 3D printer, like me) to repeatedly and exactly copy their own or somebody else's handwriting. There are many applications for this file format, such as:
* Mass-producing personalized letters (ex., handwritten invitations, thank you cards, etc.), where only a few components change from letter-to-letter (i.e., the recipient's name, which the user can write in manually).
* Replicating a signature without need for the signer's presence (so long as the GCODE is intentionally used and validated by the signer or an authorized representative appointed by the signer).

### SVG Format (in progress)
SVG files are primarily used for graphics, and are an extremely lightweight file format. From my research, no program exists with the sole purpose of converting a hand-made drawing or handwriting into an SVG file format. With an SVG handwriting or drawing file, someone can:
* Display that handwriting or drawing on a webpage
  * The extremely light file size allows for high webpage responsiveness.
  * Great for displaying generally hard-to-digitize information, such as complex math or drawings.
* Create an easily-transferrable digital signature (so long as the SVG file is intentionally used and validated by the signer or an authorized representative appointed by the signer) for signing digital documents.

### XML Format (incomplete)
Storing the handwriting data in the specified XML format allows you to take your own handwriting data and turn it into data similar to that seen in the [IAM On-Line Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-on-line-handwriting-database). This data format includes the time taken for each stroke, as well as the writer's location, name, and (optionally) other user data like age or finger-length, making it highly valuable for statistical analysis and answering questions like: 
* Does finger length correlate with writing speed? 
* What combinations of letters take the longest to write? 
* Are certain writing styles faster than others?
* How does an elementary school student's handwriting improve over time? How, fundamentally, is it improving? Are they writing faster? More legibly? Both? What letters take the longest to improve on?

Another use, and the one I am most interested in, is using this XML format to train an AI model, [like this one](https://github.com/sjvasquez/handwriting-synthesis), to allow the model to replicate your handwriting. The uses for this are vast, including, but not limited to:
* Fully AI-generated (including what is being written) hyper-realistic writing
* Mass producing personalized handwritten letters (via AI or auto-fill scripts) with no need for user intervention
* A step-by-step, fully-automated, browser-based AI writing instructor for teaching people of all ages how to write in new styles or foreign languages.
* Training for an automatic handwriting transcription software

### Making Handwriting Data Accessible (incomplete)
To increase its accessibility, handwriting data will be uploaded to an online database hosted on the cloud. Currently, I plan to use MongoDB's Atlas cloud database due to its intuitive API's. This will allow anyone to upload (with validation) or download handwriting data as desired. 

## Retrieving Data (incomplete)
As previously stated, I plan to use MongoDB's Atlas cloud database to host the handwriting data online. MongoDB allows data to be accessed through indexing, allowing users to retrieve exactly the data they need. 
