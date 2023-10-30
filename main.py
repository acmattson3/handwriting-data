### INCLUDES ###
import cv2 as cv # For windows
import numpy as np # For windows
from uuid import uuid4 # For unique form IDs
from datetime import datetime # For timestamps
from get_data import GetData # For data collection and processing


### CONSTANTS ###
PROMPTS_DIR="prompts/writing_prompts.txt"
PIX_PER_MM=1080/195 # Pixels per mm for my screen
#DRAW_LEN,DRAW_WID=int(235*PIX_PER_MM),int(235*PIX_PER_MM) # For drawing window == print bed
DRAW_LEN,DRAW_WID=1200,200
TEXT_LEN,TEXT_WID=1000,100
SCREEN_RES_X, SCREEN_RES_Y=1920,1080


### GLOBAL VARIABLES ###
writing=False
mouse_x,mouse_y=0,0
prev_x,prev_y=0,0
# For tracking horiz/vert lines
orig_x,orig_y=0,0 
has_same_x,has_same_y=False,False
is_paused=False
# Holds all strokes (list of lists of tuples)
stroke_list=[] # [ [(x,y), (x,y)], [(x,y), (x,y)] ]
# Current continuous stroke, list of tuples
curr_stroke=[]  # [(x,y), (x,y)]


### FUNCTIONS ###
# Draw a line, display info, store data.
def make_line(img, start, end, display_text=""):
    global stroke_list
    global curr_stroke

    cv.line(img, (start[0], start[1]), (end[0],end[1]), (255,255,255), 2) 
    if display_text:
        print(end[0], end[1], display_text, sep='\t')
    else:
        print(end[0], end[1], sep='\t')
    
    curr_stroke.append(start)
    # No end; start of next is end of current.

    # Store line data in memory here based on display text
    if display_text=="Up":
        curr_stroke.append(end)
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
    global mouse_x, mouse_y
    global prev_x, prev_y
    global orig_x, orig_y
    global has_same_x, has_same_y
    global is_paused
    
    if x < 0 or y < 0 or x > DRAW_LEN or y > DRAW_WID:
        return

    if is_paused:
        return

    if event == cv.EVENT_LBUTTONDOWN: 
        writing=True
        if (mouse_x!=0 and mouse_y!=0):
            prev_x,prev_y=mouse_x,mouse_y
        else:
            prev_x,prev_y=x,y
        mouse_x,mouse_y=x,y

    if event == cv.EVENT_LBUTTONUP: 
        if has_same_x:
            has_same_x=False
            make_line(draw_image, (prev_x, orig_y), (prev_x, prev_y))
        if has_same_y:
            has_same_y=False
            make_line(draw_image, (orig_x, prev_y), (prev_x,prev_y)) 

        make_line(draw_image, (x,y), (prev_x,prev_y), "Up")
        mouse_x,mouse_y=0,0
        orig_x,orig_y=0,0
        prev_x,prev_y=0,0
        writing=False
        
    if event == cv.EVENT_MOUSEMOVE and writing:
        prev_x,prev_y=mouse_x,mouse_y
        mouse_x,mouse_y=x,y
        if writing:
            if mouse_x==prev_x: # We're drawing a vertical line.
                if not has_same_x: # Starting a vertical line.
                    has_same_x=True
                    orig_y=mouse_y # For drawing line from start
                    make_line(draw_image, (prev_x, prev_y), (mouse_x,mouse_y), "Started vertical!") 
                elif has_same_x and (abs(mouse_y-orig_y)<abs(prev_y-orig_y)):
                    has_same_x=False
                    make_line(draw_image, (prev_x,orig_y), (prev_x,prev_y), "Backtracking!") 

            else: # Not drawing a vertical line
                if has_same_x: # If we were,
                    has_same_x=False # we aren't anymore.
                    make_line(draw_image, (prev_x,orig_y), (prev_x,prev_y)) 
            
            if mouse_y==prev_y: # We're drawing a horizontal line.
                if not has_same_y: # Starting horizontal line
                    has_same_y=True
                    orig_x=mouse_x # For drawing horizontal line from start
                    make_line(draw_image, (prev_x,prev_y), (mouse_x,mouse_y), "Started horizontal!")
                elif has_same_y and (abs(mouse_x-orig_x)<abs(prev_x-orig_x)):
                    has_same_y=False
                    make_line(draw_image, (orig_x, prev_y), (prev_x,prev_y), "Backtracking!") 

                
            else:
                if has_same_y:
                    has_same_y=False
                    make_line(draw_image, (orig_x, prev_y), (prev_x,prev_y))

            if not (has_same_y or has_same_x):
                make_line(draw_image, (prev_x, prev_y), (mouse_x,mouse_y))


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
    font_color=(255, 255, 255)
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
    # Begin loop until prompts answered
    curr_prompt=0
    curr_id=None
    while prompt_text:
        cv.imshow(draw_window, draw_image)
        cv.imshow(text_window, text_image)

        key=cv.waitKey(33)

        if key==27: # ESC to stop
            break

        elif key==13: # ENTER for next prompt
            print("Save time:", data.get_time())
            
            if (curr_prompt != 0):
                # data.store(curr_id, prompt_text, stroke_list) # Start a new file
                print("Number of strokes:", len(stroke_list))
        
            stroke_list=[]

            # Generate new data for current prompt
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

        elif key != -1:
            print(f"That key, ID {key}, doesn't do anything yet.")
            print("P\t=> Pause")
            print("ENTER\t=> Get the next prompt")
            print("Z\t=> Restart current prompt")
            print("G\t=> Generate GCODE from current drawing")
            print("ESC\t=> Quit")

    cv.destroyAllWindows()
    if not prompt_text:
        input("All prompts written! Press enter to exit.")
    f.close()
