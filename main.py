''' 
Main for handwriting-data
Uses OpenCV to display prompts and create
writing data through simple drawing software.
'''


### INCLUDES ###
import cv2 as cv # For windows
import numpy as np # For windows
from uuid import uuid4 # For unique form IDs
from datetime import datetime # For timestamps
from get_data import GetData # For data collection and processing
from coordinates import * # For classes Coord and StrokeCoord


### CONSTANTS ###
PROMPTS_DIR="prompts/writing_prompts.txt"
PIX_PER_MM=1080/195 # Pixels per mm for my screen
DRAW_LEN,DRAW_WID=int(186*PIX_PER_MM),int(135*PIX_PER_MM) # For drawing window == print bed
#DRAW_LEN,DRAW_WID=1200,200
TEXT_LEN,TEXT_WID=1000,100
SCREEN_RES_X, SCREEN_RES_Y=1920,1080
DRAW_COLOR = (255,255,255)


### GLOBAL VARIABLES ###
writing=False
mouse=Coord(0,0)
prev=Coord(0,0)
# For tracking horiz/vert lines
orig=Coord(0,0)
has_same_x,has_same_y=False,False
is_paused=False
# Holds all strokes (list of lists of StrokeCoords)
stroke_list=[] # [ [S, S], [S, S] ]
# Current continuous stroke, list of StrokeCoord's
curr_stroke=[]  # [S, S]


### FUNCTIONS ###
# Returns current time
def get_time():
    now=datetime.now()
    save_time=(now.year * 12 + now.month) * 31 + now.day
    save_time=(save_time * 24 + now.hour) * 60 + now.minute
    save_time=(save_time * 60 + now.second) + (now.microsecond / 1000000.0)
    return save_time

# Draw a line, display info, store data.
def make_line(img, start, end, display_text=""):
    global stroke_list
    global curr_stroke

    cv.line(img, (start.x,start.y), (end.x,end.y), DRAW_COLOR, 2) 
    if display_text:
        print(end.x, end.y, display_text, sep='\t')
    else:
        print(end.x, end.y, sep='\t')
    
    curr_stroke.append(StrokeCoord(start, get_time()))
    # No end; start of next line is end of current line.

    # Store line data in memory here based on display text
    if display_text=="Up":
        curr_stroke.append(StrokeCoord(end, get_time()))
        stroke_list.append(curr_stroke)
        curr_stroke=[]

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

    now=Coord(x,y)
    
    if x < 0 or y < 0 or x > DRAW_LEN or y > DRAW_WID:
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
    data = GetData(collecting=True)

    # Configure drawing and text windows
    draw_window="Writing Pad"
    text_window="Text Box"
    draw_size=DRAW_WID, DRAW_LEN, 3
    draw_image=np.zeros(draw_size, dtype=np.uint8)
    text_size=TEXT_WID,TEXT_LEN,3
    text_image=np.zeros(text_size, dtype=np.uint8)

    # Initialize drawing and text windows
    cv.namedWindow(draw_window)
    cv.namedWindow(text_window)

    # Connect mouse event function
    cv.setMouseCallback(draw_window, click_event) 

    # Font settings
    text_start_offset=(0, int(TEXT_WID/2))
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

    cv.imshow(draw_window, draw_image)
    cv.imshow(text_window, text_image)
    cv.moveWindow(draw_window, # Center draw window
                  int(SCREEN_RES_X-DRAW_LEN-50), 
                  int(SCREEN_RES_Y/2-DRAW_WID-50)
                  )
    cv.moveWindow(text_window, # Center draw window
                  int(SCREEN_RES_X-TEXT_LEN-50), 
                  int(SCREEN_RES_Y/2-TEXT_WID/2-400)
                  )
    
    # Begin loop until all prompts answered
    curr_prompt=0
    curr_id=None
    while prompt_text:
        cv.imshow(draw_window, draw_image)
        cv.imshow(text_window, text_image)

        key=cv.waitKey(33)

        if key==27: # ESC to stop
            break

        elif key==13: # ENTER for next prompt
            print("Save time:", get_time())
            
            if (curr_prompt != 0):
                # data.store(curr_id, prompt_text, stroke_list) # Start a new file
                print("Number of strokes:", len(stroke_list))
        
            stroke_list=[]

            # Generate new data for current prompt
            # # We should create an ID using the writer ID and prompt ASCII text in hash function
            curr_id=uuid4() 
            
            # Get new prompt
            prompt_text=f.readline()[:-1]
            curr_prompt+=1
            
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

        elif key==122: # Z to restart current prompt.
            print("Restarting prompt number", curr_prompt)
            print("Prompt ID:", curr_id)
            draw_image=np.zeros(draw_size, dtype=np.uint8)
            stroke_list=[]

        elif key==103: # G to generate GCODE for current draw window.
            filename=data.generate_gcode(stroke_list, "current_window", DRAW_WID)
            print(f"Generated GCODE. Filename: {filename}")
            pause_drawing()

        elif key==115: # S to generate SVG for current draw window
            filename=data.generate_svg(stroke_list, "current_window", DRAW_LEN, DRAW_WID)
            print(f"Generated SVG. Filename: {filename}")
            pause_drawing()

        elif key != -1: # Unassigned key pressed
            print(f"That key, ID {key}, doesn't do anything yet.")
            print("ESC\t=> Quit")
            print("ENTER\t=> Get the next prompt")
            print("P\t=> Pause drawing window")
            print("Z\t=> Restart current prompt")
            print("G\t=> Generate GCODE from current drawing")
            print("S\t=> Generate SVG from current drawing")

    cv.destroyAllWindows()
    if not prompt_text:
        input("All prompts written! Press enter to exit.")
    f.close()
