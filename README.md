# handwriting-data
A way to gather, store, and retrieve data for the [handwriting-synthesis](https://github.com/sjvasquez/handwriting-synthesis) AI. 

## Gathering Data
The data gathering portion involves a basic OpenCV drawing program used to collect pixel data of a user's pen strokes as they write. 

The program begins by asking for the user's information, including their name and general location. The program also automatically gathers the start/end time, program version, and drawing window size. Then, the interactive writing program launches. The text window provides the user with a prompt. The user writes this prompt using a digital tablet (such as a [Gaomon Tablet](https://gaomon.net/)), writing within the drawing window. As the user writes, the program records the resulting cursor events (mouse up/down) and movement data (x/y coordinates and timing) in memory.

## Storing Data (in progress)
After the user completes a prompt or writes something custom, that data can be stored in a few different ways:
1. A GCODE file format, given a user's screen's pixel/mm ratio (by pressing 'g' on the keyboard)
2. An XML file format, as seen [here](https://fki.tic.heia-fr.ch/static/iamondb/strokesz.xml) (by pressing 'enter' on the keyboard)
3. An SVG file format (by pressing 's' on the keyboard)

### GCODE Format
Converting the writing data to GCODE exactly copies the user's input data, millimeter by millimeter, into GCODE. This allows users with a CNC writing robot (or modified 3D printer, like me) to repeatedly and exactly copy their own or somebody else's handwriting. There are many applications for this file format, such as:
* Mass-producing personalized letters (ex., handwritten invitations, thank you cards, etc.), where only a few components change from letter-to-letter (i.e., the recipient's name, which the user can write in manually).
* Replicating a signature without need for the signer's presence (so long as the GCODE is intentionally used and validated by the signer or an authorized representative appointed by the signer).

### SVG Format

### XML Format
Storing the handwriting data allows for a vast set of usages for the handwriting data. 

## Retrieving Data (incomplete)
