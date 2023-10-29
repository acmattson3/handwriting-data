import cv2 as cv # For windows
import numpy as np # For windows
from uuid import uuid4 # For unique form ID
from datetime import datetime # For timestamps
import get_data

### CONSTANTS ###
PROMPTS_DIR="prompts/writing_prompts.txt"
DRAW_LEN,DRAW_WID = 1200,200
TEXT_LEN,TEXT_WID = 1000,100

### GLOBAL VARIABLES ###
writing=False
mouse_x,mouse_y=0,0
prev_x,prev_y=0,0
# For tracking horiz/vert lines
orig_x,orig_y=0,0 
has_same_x,has_same_y=False,False
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

    # TODO: On every draw line, put line data into memory.
    if event == cv.EVENT_LBUTTONDOWN: 
        print("Down:", x, y, sep='\t') 
        writing=True
        if (mouse_x!=0 and mouse_y!=0):
            prev_x,prev_y=mouse_x,mouse_y
        else:
            prev_x,prev_y=x,y
        mouse_x,mouse_y=x,y

    if event == cv.EVENT_LBUTTONUP: 
        print("Up:", x, y, sep='\t') 
        if has_same_x:
            has_same_x=False
            cv.line(draw_image, (prev_x, orig_y), (prev_x,prev_y), (255,255,255), 2) 
        if has_same_y:
            has_same_y=False
            cv.line(draw_image, (orig_x, prev_y), (prev_x,prev_y), (255,255,255), 2) 

        cv.line(draw_image, (x,y), (prev_x,prev_y), (255,255,255), 2)
        mouse_x,mouse_y=0,0
        orig_x,orig_y=0,0
        prev_x,prev_y=0,0
        writing=False
        
    if event == cv.EVENT_MOUSEMOVE and writing:
        prev_x,prev_y=mouse_x,mouse_y
        mouse_x,mouse_y=x,y
        if writing:
            if mouse_x==prev_x:
                if not has_same_x:
                    has_same_x=True
                    orig_y=mouse_y
                    cv.line(draw_image, (prev_x, prev_y), (mouse_x,mouse_y), (255,255,255), 2) 
                    print("Started vertical line!")
            else:
                if has_same_x:
                    has_same_x=False
                    cv.line(draw_image, (prev_x, orig_y), (prev_x,prev_y), (255,255,255), 2) 
                    print(prev_x, prev_y, sep='\t')
            
            if mouse_y==prev_y:
                if not has_same_y:
                    has_same_y=True
                    orig_x=mouse_x
                    cv.line(draw_image, (prev_x, prev_y), (mouse_x,mouse_y), (255,255,255), 2)
                    print("Started horizontal line!")
                
            else:
                if has_same_y:
                    has_same_y=False
                    cv.line(draw_image, (orig_x, prev_y), (prev_x,prev_y), (255,255,255), 2) 
                    print(prev_x, prev_y, sep='\t')

            if not (has_same_y or has_same_x):
                cv.line(draw_image, (prev_x, prev_y), (mouse_x,mouse_y), (255,255,255), 2) 
                print(x, y, sep='\t')


if __name__ == "__main__":
    get_data.collect(False) # Disable data collection

    # Get ID of writer on startup
    writer_id=get_data.writer_id()

    # Configure drawing and text windows
    draw_window = "Writing Pad"
    text_window = "Text Box"
    draw_size = DRAW_WID, DRAW_LEN, 3
    draw_image = np.zeros(draw_size, dtype=np.uint8)
    text_size = TEXT_WID,TEXT_LEN,3
    text_image = np.zeros(text_size, dtype=np.uint8)

    # Initialize drawing and text windows
    cv.namedWindow(draw_window)
    cv.namedWindow(text_window)

    # Connect mouse event function
    cv.setMouseCallback(draw_window, click_event) 

    # Font settings
    text_start_offset = (0, int(TEXT_WID/2))
    font_style = cv.FONT_HERSHEY_DUPLEX
    font_size = 0.6
    font_color = (255, 255, 255)
    font_thickness = 1

    f = open(PROMPTS_DIR, "r")
    prompt_text="Click into the writing Pad and press enter to start!"

    cv.putText(
            img = text_image,
            text = prompt_text,
            org = text_start_offset,
            fontFace = font_style,
            fontScale = font_size,
            color = font_color,
            thickness = font_thickness
            )

    # Begin loop until prompts answered
    curr_prompt=0
    while prompt_text:
        cv.imshow(draw_window, draw_image)
        cv.imshow(text_window, text_image)
        key = cv.waitKey(33)
        if key==27: # ESC to stop
            break
        elif key==13: # ENTER for next prompt
            # Store previous prompt's data
            now = datetime.now()
            save_time = (now.year * 12 + now.month) * 31 + now.day
            save_time = (save_time * 24 + now.hour) * 60 + now.minute
            save_time = (save_time * 60 + now.second) + (now.microsecond / 1000000.0)
            print("Save Time: ", save_time)
            
            if (curr_prompt != 0):
                # get_data.store() # Start a new file
                pass # Store previous prompt's data here (move it out of memory?)
        
            # Generate new data for current prompt
            new_id=uuid4()
            print("New ID:", new_id)
        
            # Get new prompt
            prompt_text=f.readline()[:-1]
            curr_prompt+=1
            
            # Clear screens
            draw_image = np.zeros(draw_size, dtype=np.uint8)
            text_image = np.zeros(text_size, dtype=np.uint8)
            
            # Display new prompt
            print("Next prompt! Number", curr_prompt)
            cv.putText( # Put new prompt in text window.
                img = text_image,
                text = prompt_text,
                org = text_start_offset,
                fontFace = font_style,
                fontScale = font_size,
                color = font_color,
                thickness = font_thickness
                )
            
        elif key==112: # P to pause; semi-functional; doesn't work well with time.
            print("Paused! Press any key in drawing window to resume.")
            is_paused=True
            cv.waitKey(-1)
            print("Resumed! You can continue drawing.")
            is_paused=False

        elif key != -1:
            print("That key doesn't do anything yet.")
            print("Press P to pause.")
            print("Press ENTER for the next prompt.")
            print("Press ESC to exit.")

    cv.destroyAllWindows()
    if not prompt_text:
        input("All prompts written! Press enter to exit.")
    f.close()