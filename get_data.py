from datetime import datetime

# Begin class GetData
class GetData:
    __z_lift=1.5
    __pix_per_mm=1080/195 # 1080 pixel tall screen, 195mm long
    __scale_factor=1/__pix_per_mm

    __start_gcode=["G28\n",
                   f"G01 Z{__z_lift} F500\n",
                   f"G01 X20 Y0 (avoid clip)",
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
    
    # Returns current time
    def get_time(self):
        now=datetime.now()
        save_time=(now.year * 12 + now.month) * 31 + now.day
        save_time=(save_time * 24 + now.hour) * 60 + now.minute
        save_time=(save_time * 60 + now.second) + (now.microsecond / 1000000.0)
        return save_time
    
    # Generates 3D printer GCODE based on raw stroke data
    def generate_gcode(self, stroke_list, id_string, draw_wid, feedrate=2000):
        filename="autogen_"+id_string+".gcode"
        with open(filename, "w") as f:
            f.write("(Start GCODE)\n")
            f.writelines(self.__start_gcode)

            for i, stroke in enumerate(stroke_list):
                f.write(f"(Starting stroke #{i+1})\n")

                init_stroke_x,init_stroke_y=stroke[0]

                f.write(f"G01 X{init_stroke_x*self.__scale_factor} Y{(draw_wid-init_stroke_y)*self.__scale_factor} Z{self.__z_lift} F{feedrate}\n")
                f.write("G01 Z0 F500\n")
                f.write(f"G01 F{feedrate}")
                for x,y in stroke[1:]:
                    f.write(f"G01 X{x*self.__scale_factor} Y{(draw_wid-y)*self.__scale_factor} Z0\n")
                f.write(f"G01 Z{self.__z_lift} F500\n\n")

            f.write("(End GCODE)\n")
            f.writelines(self.__end_gcode)

        return filename

    # Stores all form data in XML format (for handwriting-synthesis processing)
    #def store(self, stroke_list, curr_id, ...):
