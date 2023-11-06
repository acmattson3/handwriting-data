''' Main for handwriting-data
* Uses OpenCV to display prompts and create
  writing data through simple drawing software.
* Run this file to run the data collection program.
'''


### INCLUDES ###
import cv2 as cv # For windows
import numpy as np # For windows
from get_data import GetData # For data collection and processing
from get_data import get_choice, get_time
from coordinates import * # For classes Coord and StrokeCoord
from config import * # Import user-dependent constants

### GLOBAL VARIABLES ###
writing=False
mouse=Coord(0,0)
prev=Coord(0,0)
# For tracking horiz/vert lines
orig=Coord(0,0)
has_same_x,has_same_y=False,False
is_paused=False
# Holds all strokes (list of lists of StrokeCoord's)
strokes_list=[] # [ [S, S], [S, S] ]
# Current continuous stroke, list of StrokeCoord's
curr_strokes=[]  # [S, S]
draw_height=DRAW_HEIGHT
draw_wid=DRAW_WID


### OPENCV DEPENDENT FUNCTIONS ###
# Draw a line, display info, store data.
def make_line(img, start, end, display_text=""):
    global strokes_list
    global curr_strokes

    cv.line(img, (start.x,start.y), (end.x,end.y), DRAW_COLOR, 2)
    if DEBUGGING:
        if display_text:
            print(end.x, end.y, display_text, sep='\t')
        else:
            print(end.x, end.y, sep='\t')
    
    curr_strokes.append(StrokeCoord(start, get_time()))
    # No end; start of next line is end of current line.

    # Store line data in memory here based on display text
    if display_text=="Up":
        curr_strokes.append(StrokeCoord(end, get_time()))
        strokes_list.append(curr_strokes)
        curr_strokes=[]

# Pause drawing window. 
def pause_drawing():
    global is_paused

    print("Paused! Press any key in drawing window to resume.")
    is_paused=True
    cv.waitKey(-1)
    print("Resumed! You can continue drawing.")
    is_paused=False

# When a mouse event occurs, this function is called.
def click_event(event, x, y, flags, params): 

    # Required globals
    global writing
    global mouse, prev, orig
    global has_same_x, has_same_y
    global is_paused
    global draw_wid, draw_height

    now=Coord(x,y)
    
    if x < 0 or y < 0 or x > draw_wid or y > draw_height:
        return

    if is_paused:
        return

    if event == cv.EVENT_LBUTTONDOWN: 
        writing=True
        if (mouse.x!=0 and mouse.y!=0):
            prev.copy(mouse)
        else:
            prev.copy(now)
        mouse.copy(now)

    if event == cv.EVENT_LBUTTONUP: 
        if has_same_x:
            has_same_x=False
            make_line(draw_image, Coord(prev.x, orig.y), prev)
        if has_same_y:
            has_same_y=False
            make_line(draw_image, Coord(orig.x, prev.y), prev) 

        make_line(draw_image, now, prev, "Up")
        mouse.zero()
        orig.zero()
        prev.zero()
        writing=False
        
    if event == cv.EVENT_MOUSEMOVE and writing:
        prev.copy(mouse)
        mouse.copy(now)
        if writing:
            if mouse.x==prev.x: # We're drawing a vertical line.
                if not has_same_x: # Starting a vertical line.
                    has_same_x=True
                    orig.y=mouse.y # For drawing vertical line from start
                    make_line(draw_image, prev, mouse, "Started vertical!") 
                elif has_same_x and (abs(mouse.y-orig.y)<abs(prev.y-orig.y)):
                    has_same_x=False
                    make_line(draw_image, Coord(prev.x,orig.y), prev, "Backtracking!") 

            else: # Not drawing a vertical line
                if has_same_x: # If we were,
                    has_same_x=False # we aren't anymore.
                    make_line(draw_image, Coord(prev.x,orig.y), prev) 
            
            if mouse.y==prev.y: # We're drawing a horizontal line.
                if not has_same_y: # Starting horizontal line
                    has_same_y=True
                    orig.x=mouse.x # For drawing horizontal line from start
                    make_line(draw_image, prev, mouse, "Started horizontal!")
                elif has_same_y and (abs(mouse.x-orig.x)<abs(prev.x-orig.x)):
                    has_same_y=False
                    make_line(draw_image, Coord(orig.x, prev.y), prev, "Backtracking!") 

            else:
                if has_same_y:
                    has_same_y=False
                    make_line(draw_image, Coord(orig.x, prev.y), prev)

            if not (has_same_y or has_same_x):
                make_line(draw_image, prev, mouse)


### MAIN ###
if __name__ == "__main__":
    validate_configs() # Check that configs are set up properly

    data = GetData(True if get_choice("Do you wish to gather data?", 'y', 'n')=='y' else False)

    use_prompts=get_choice("Do you wish to use prompts?", 'y', 'n')

    draw_size=DRAW_HEIGHT, DRAW_WID, 3
    extra_data={}
    if use_prompts=='y':
        display_text=True
        if data.is_collecting():
            collect_extra=get_choice("Would you like to collect other user data?", 'y', 'n')
            if collect_extra=='y':
                while (collect_extra=='y'):
                    new_data_key=input("Please enter the data category name: ")
                    new_data_val=input(f"Please enter the value of {new_data_key}: ")
                    extra_data[new_data_key]=new_data_val
                    collect_extra=get_choice("Would you like to collect any other user data?", 'y', 'n')
    else:
        display_text=False
        print("Please specify desired draw window size.")
        use_pixels=get_choice("Do you wish to define size by pixels or mm?", 'px', 'mm')

        # Ensure valid window size
        valid_size=False
        while not valid_size:
            try:
                if use_pixels=='px':
                    draw_height=int(input("Enter window height in pixels: "))
                    draw_wid=int(input("Enter window width in pixels: "))
                else:
                    draw_height=int(int(input("Enter window height in mm: "))*PIX_PER_MM)
                    draw_wid=int(int(input("Enter window width in mm: "))*PIX_PER_MM)

                assert draw_height>0
                assert draw_wid>0
                valid_size=True
            except:
                print("Invalid entry. Please enter a positive integer number.")
            
        draw_size=draw_height, draw_wid, 3

    # Configure drawing and text windows
    draw_window="Writing Pad"
    draw_image=np.zeros(draw_size, dtype=np.uint8)

    # Initialize drawing and text windows
    cv.namedWindow(draw_window)

    # Connect mouse event function
    cv.setMouseCallback(draw_window, click_event) 

    cv.imshow(draw_window, draw_image)

    # Text box preparation
    if display_text:
        text_window="Text Box"
        text_size=TEXT_HEIGHT,TEXT_WID,3
        text_image=np.zeros(text_size, dtype=np.uint8)
        cv.namedWindow(text_window)
        # Font settings
        text_start_offset=(0, int(TEXT_HEIGHT/2))
        font_style=cv.FONT_HERSHEY_DUPLEX
        font_size=0.6
        font_color=DRAW_COLOR
        font_thickness=1

        f=open(PROMPTS_DIR, "r")
        prompt_text="Click into the writing Pad and press enter to start!"

        cv.putText(
                img=text_image,
                text=prompt_text,
                org=text_start_offset,
                fontFace=font_style,
                fontScale=font_size,
                color=font_color,
                thickness=font_thickness
                )
        cv.imshow(text_window, text_image)
    
    # Begin loop until all prompts answered
    curr_prompt=0
    curr_id=None
    while True:
        if display_text and not prompt_text:
            print(f"Empty prompt: Prompt #{curr_prompt}. Indicates end of file.")
            break

        cv.imshow(draw_window, draw_image)
        if display_text:
            cv.imshow(text_window, text_image)

        key=cv.waitKey(10)

        if key==27: # ESC to stop
            print("Exiting program...")
            break

        elif key==13 and display_text: # ENTER for next prompt
            print("Save time:", get_time())
            
            if (curr_prompt != 0):
                data.generate_json(strokes_list, prompt_text, curr_id, curr_prompt, extra_data) # Save previous prompt data
                if DEBUGGING:
                    print("Number of strokes:", len(strokes_list))
        
            strokes_list=[]
            
            # Get new prompt
            prompt_text=f.readline()[:-1]
            curr_prompt+=1

            # Generate new data for current prompt

            # Get new ID
            curr_id=data.get_id(prompt_text)
            
            # Clear screens
            draw_image=np.zeros(draw_size, dtype=np.uint8)
            text_image=np.zeros(text_size, dtype=np.uint8)
            
            # Display new prompt
            print("\nNext prompt! Number", curr_prompt)
            print("Prompt ID:", curr_id)
            cv.putText( # Put new prompt in text window.
                img=text_image,
                text=prompt_text,
                org=text_start_offset,
                fontFace=font_style,
                fontScale=font_size,
                color=font_color,
                thickness=font_thickness
                )
            
        elif key==112: # P to pause.
            pause_drawing()

        elif key==122: # Z to restart current prompt/clear display.
            if display_text:
                print("Restarting prompt number", curr_prompt)
                print("Prompt ID:", curr_id)
            draw_image=np.zeros(draw_size, dtype=np.uint8)
            print("Display cleared.")
            strokes_list=[]

        elif key==103: # G to generate GCODE for current draw window.
            filename=data.generate_gcode(strokes_list, "current_window", draw_height)
            print(f"Generated GCODE. Filename: {filename}")
            pause_drawing()

        elif key==115: # S to generate SVG for current draw window
            filename=data.generate_svg(strokes_list, "current_window", draw_wid, draw_height)
            print(f"Generated SVG. Filename: {filename}")
            pause_drawing()

        elif key != -1: # Unassigned key pressed
            print(f"That key, ID {key}, doesn't do anything yet.")
            print("ESC\t=> Quit")
            if display_text:
                print("ENTER\t=> Get the next prompt")
            print("P\t=> Pause drawing window")
            print("Z\t=> Restart current prompt/Clear display")
            print("G\t=> Generate GCODE from current drawing")
            print("S\t=> Generate SVG from current drawing")

    cv.destroyAllWindows()
    if display_text and not prompt_text:
        input("All prompts complete! Exiting...")
        f.close()