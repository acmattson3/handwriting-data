'''
get_data for handwriting-data
Manages all data collection and processing from drawing software
'''

from datetime import datetime
import svgwrite # For writing SVG files

# Begin class GetData
class GetData:
    __z_lift=1.5
    __pix_per_mm=1080/195 # 1080 pixel tall screen, 195mm long
    __scale_factor=1/__pix_per_mm

    __start_gcode=["G28\n",
                   f"G01 Z{__z_lift} F500\n",
                   f"G01 X0 Y20 (avoid clip)",
                   "\n"]
    __end_gcode=["G01 Z1.5 F500\n",
                 f"G01 X10 Y{235/2} (avoid clips)",
                 "G01 X10 Y235 (present page)\n"]

    # Ctor
    # Get's ID of writer, if we are collecting data.
    def __init__(self, collecting=True):
        self.__collecting=collecting
        self.__wid=self.__new_writer_id()

    # Get ID of writer
    def __new_writer_id(self):
        if not self.__collecting:
            return ""
        writer_id=input("Please enter your name: ")
        input_string="You entered: '" + writer_id + "'. Is this correct? (y/n) "
        is_correct = input(input_string)
        while is_correct != 'y':
            writer_id=input("Please enter your name: ")
            input_string="You entered: '" + writer_id + "'. Is this correct? (y/n) "
            is_correct = input(input_string)
        
        return writer_id

    # Returns writer ID if someone needs it.
    def get_writer_id(self): 
        return self.__wid
    
    # Store the data in GCODE format (for use with CNC machine or 3D printer)
    def generate_gcode(self, stroke_list, id_string, draw_wid, feedrate=2000):
        filename="autogen_"+id_string+".gcode"
        with open(filename, "w") as f:
            f.write("(Start GCODE)\n")
            f.writelines(self.__start_gcode)

            for i, stroke in enumerate(stroke_list):
                f.write(f"(Starting stroke #{i+1})\n")

                first_x,first_y=stroke[0].tuplize()
                
                f.write(f"G01 X{first_x*self.__scale_factor} Y{(draw_wid-first_y)*self.__scale_factor} Z{self.__z_lift} F{feedrate}\n")
                f.write("G01 Z0 F500\n")
                f.write(f"G01 F{feedrate}")
                for p in stroke[1:]:
                    f.write(f"G01 X{p.x*self.__scale_factor} Y{(draw_wid-p.y)*self.__scale_factor} Z0\n")
                f.write(f"G01 Z{self.__z_lift} F500\n\n")

            f.write("(End GCODE)\n")
            f.writelines(self.__end_gcode)

        return filename
    
    # Store the data in SVG format
    def generate_svg(self, stroke_list, id_string, draw_len, draw_wid):
        filename="autogen_"+id_string+".svg"
            
        dwg = svgwrite.Drawing(filename=filename, profile='full')
        dwg.viewbox(width=draw_wid, height=draw_len)
        dwg.add(dwg.rect(insert=(0, 0), size=(draw_wid, draw_len), fill='white'))
        
        curr_path=""
        for stroke in stroke_list:
            first_x,first_y=stroke[0].tuplize()
            curr_path+=f"M{first_x},{first_y} "
            for p in stroke[1:]:
                curr_path+=f"L{p.x},{p.y} "

        path = svgwrite.path.Path(curr_path)
        path = path.stroke(color="black", width=2, linecap='round').fill("none")
        dwg.add(path)
        
        dwg.save()

        return filename

    # Stores all form data in XML format (for handwriting-synthesis processing)
    #def store(self, stroke_list, curr_id, ...):
