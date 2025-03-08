''' prepare_style for handwriting-data
Meant to generate styles, but not working.
'''

import numpy as np
import svgpathtools
import os
import glob

def get_files_of_type(file_ext):
    # Set the current directory
    current_directory=os.getcwd()

    # Pattern for file_ext files
    pattern=f"*.{file_ext}"

    # Get a list of all file_ext files in the current directory
    return glob.glob(os.path.join(current_directory, pattern))

# Gets choice, either op1 and op2, from user.
# **MODIFIED FROM get_data.py**
def get_choice_range(query, op_range):
    op_val=input(f"{query} ({op_range[0]} - {op_range[-1]}): ")

    while op_val not in op_range:
        print(f"Invalid input. Enter in range {op_range[0]} to {op_range[-1]}")
        op_val=input(f"{query} ({op_range[0]} - {op_range[-1]}): ")

    return op_val

def select_from_elems(elems):
    print("Please choose one:")
    for i, elem in enumerate(elems):
        print(f"{i+1}: {elem}")
    return elems[get_choice_range("Choice: ", range(1, len(elems)))]


if __name__=="__main__":
    input("WARNING! This script is currently not working! Press enter to try anyways.")

    all_svgs=get_files_of_type("svg")

    if len(all_svgs) > 1: # More than one SVG: Choose one
        chosen_svg=select_from_elems(all_svgs)
    elif len(all_svgs) == 1: # One SVG present (must use that one)
        chosen_svg=all_svgs[0]
    elif len(all_svgs) <= 0: # No SVG's present
        print("No SVG files to choose from.")
        exit(0)

    paths, attributes=svgpathtools.svg2paths(chosen_svg)

    # first we concat all of the stokes into a single string. Some SVG files will have multiple path elements.
    strokes=''
    for k, v in enumerate(attributes):
        if 'd' in v:
            strokes=strokes + ' ' + v['d']

    # consolidate the ',' and ' ' deliniation
    strokes=strokes.replace(',',' ').split(' ')
    print("Strokes:", strokes)
    # build out our 3d array. First element is x, second is y and 3rd is the command (move M or line L) of the next line.
    stroke_arr=[]
    for k, v in enumerate(strokes):
        print("v:", v)
        v=v.strip()
        if not v: continue
        
        v=v[0]

        # TODO: FIX ME

        if v == 'M' or v == 'L' or v == 'm' or v == 'l':
            print("Entering")
            op=0.0
            shifted_key=k+3 #this shift is because the command on this line is for the next set of coordinates
            if shifted_key < len(strokes):
                shifted_op=strokes[shifted_key].strip()
                op=1.0 if shifted_op == 'M' or shifted_op == 'm' else 0.0
            # y is flipped so we multiple by -1
            print("Appending")
            stroke_arr.append([float(strokes[k+1]),-1*float(strokes[k+2]),float(op)])
            
    print("Stroke arr:", stroke_arr)

    # start the pen at 0,0
    stroke_arr[0][0]=0.0
    stroke_arr[0][1]=0.0

    np.save("model/style/style-15-strokes.npy",np.array(stroke_arr))