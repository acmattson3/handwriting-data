''' get_data for handwriting-data
* Manages all data collection and processing from drawing software
'''

from datetime import datetime # For getting current time
import svgwrite # For writing SVG files
import json # For writing JSON files
from config import *
from os.path import isfile

### GENERAL FUNCTIONS ###
# Gets choice, either op1 and op2, from user.
def get_choice(query, op1, op2):
    op_val=input(f"{query} ({op1}/{op2}): ")

    while op_val!=op1 and op_val!=op2:
        print(f"Invalid input. Enter '{op1}' or '{op2}'")
        op_val=input(f"{query} ({op1}/{op2}): ")

    return op_val

# Returns the current time
def get_time():
    now=datetime.now()
    save_time=(now.year * 12 + now.month) * 31 + now.day
    save_time=(save_time * 24 + now.hour) * 60 + now.minute
    save_time=(save_time * 60 + now.second) + (now.microsecond / 1000000.0)
    return save_time

def gen_hash(input_string): 
    hash_num=1
    for char in input_string:
        hash_num*=int(ord(char))

        while hash_num>=10000000000000:
            hash_num=int(hash_num/len(input_string))
    
    while hash_num < 1000000000000:
        hash_num*=10

    return hash_num


### Begin class GetData ###
class GetData:
    __z_lift=1.5
    __scale_factor=1/PIX_PER_MM

    __start_gcode=["G28\n",
                   f"G01 Z{__z_lift} F500\n",
                   f"G01 X0 Y20 (avoid clip)",
                   "\n"]
    __end_gcode=["G01 Z1.5 F500\n",
                 f"G01 X0 Y{235/2} (avoid clips)",
                 "G01 X0 Y235 (present page)\n"]

    # Ctor
    # Get's ID of writer, if we are collecting data.
    def __init__(self, collecting=True):
        self.__collecting=collecting
        self.__wid=self.__new_writer_id()
        self.__curr_id=None

    def is_collecting(self):
        return self.__collecting

    # Get ID of writer
    def __new_writer_id(self):
        if not self.__collecting:
            return ""
        writer_id=input("Please enter your name: ")
        is_correct=get_choice(f"You entered: '{writer_id}'. Is this correct?", 'y', 'n')
        while is_correct != 'y':
            writer_id=input("Please enter your name: ")
            is_correct=get_choice(f"You entered: '{writer_id}'. Is this correct?", 'y', 'n')
        
        return writer_id

    # Returns writer ID if someone needs it.
    def get_writer_id(self): 
        return self.__wid
    
    # Generates a custom hash code based on writer ID and a prompt
    def get_id(self, prompt):
        hashed_string=self.__wid+prompt
        self.__curr_id=gen_hash(hashed_string)
        return self.__curr_id
    
    # Store the data in GCODE format (for use with CNC machine or 3D printer)
    def generate_gcode(self, strokes_list, id_string, draw_height, feedrate=2000):
        filename="autogen_"+id_string+".gcode"
        with open(filename, "w") as f:
            f.write("(Start GCODE)\n")
            f.writelines(self.__start_gcode)

            for i, stroke in enumerate(strokes_list):
                f.write(f"(Starting stroke #{i+1})\n")

                first_x,first_y=stroke[0].tuplize()
                
                f.write(f"G01 X{first_x*self.__scale_factor} Y{(draw_height-first_y)*self.__scale_factor} Z{self.__z_lift} F{feedrate}\n")
                f.write("G01 Z0 F500\n")
                f.write(f"G01 F{feedrate}")
                for p in stroke[1:]:
                    f.write(f"G01 X{p.x*self.__scale_factor} Y{(draw_height-p.y)*self.__scale_factor} Z0\n")
                f.write(f"G01 Z{self.__z_lift} F500\n\n")

            f.write("(End GCODE)\n")
            f.writelines(self.__end_gcode)

        return filename
    
    # Store the data in SVG format
    def generate_svg(self, strokes_list, id_string, draw_wid, draw_height):
        filename="autogen_"+id_string+".svg"
            
        dwg = svgwrite.Drawing(filename=filename, profile='full')
        dwg.viewbox(width=draw_wid, height=draw_height)
        dwg.add(dwg.rect(insert=(0, 0), size=(draw_wid,draw_height), fill='white'))
        
        curr_path=""
        for stroke in strokes_list:
            first_x,first_y=stroke[0].tuplize()
            curr_path+=f"M{first_x},{first_y} "
            for p in stroke[1:]:
                curr_path+=f"L{p.x},{p.y} "

        path = svgwrite.path.Path(curr_path)
        path = path.stroke(color="black", width=2, linecap='round').fill("none")
        dwg.add(path)
        
        dwg.save()

        return filename

    # Store the data in JSON format
    def generate_json(self, strokes_list, prompt_text, curr_id, curr_prompt, extra_data):
        if not self.__collecting:
            return ""
        data={}
        data["id"]=curr_id
        data["writer_id"]=self.__wid
        
        now=datetime.now()
        data["save_date_time"]={
            "year":int(now.year),
            "month":int(now.month),
            "day":int(now.day),
            "time":str(now.hour)+":"+str(now.minute)+":"+str(now.second)+"."+str(now.microsecond)
            }

        for key in extra_data:
            val=extra_data[key]
            data[key]=val
        data["transcription"]=prompt_text
        new_strokes_list=[[point.deformat() for point in stroke] for stroke in strokes_list]

        data["strokes"]=new_strokes_list

        json_file=json.dumps(data, indent=4)

        current_time=str(now.hour)+str(now.minute)+str(now.second)
        timestamp=str(now.year)+str(now.month)+str(now.day)+'_'+current_time
        filename=self.__wid+str(curr_prompt)+'_'+timestamp+".json"
        filepath=PROMPT_DATA_DIR+filename

        with open(filepath, "w") as f:
            f.write(json_file)
            