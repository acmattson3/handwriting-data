''' config for handwriting-data
* Contains user dependent constants
* Contains other configurable program settings
'''

# by default, screen height is -1, and resolution is -1,-1. Please change these values.

### USER CONFIGURED CONSTANTS ###
# Used to calculate pixels per millimeter value.
SCREEN_HEIGHT=-1 # The height of your screen, in millimeters.
SCREEN_RES_X,SCREEN_RES_Y=-1,-1 # The resolution of your screen (ex., 1920x1080 becomes 1920,1080)

### OTHER SETTINGS ###
DATABASE_NAME="HandwritingData"
PROMPTS_DIR="prompts/writing_prompts.txt" # The path to the prompts you wish to gather data on.
PROMPT_DATA_DIR="prompts/prompt_data/" # Data directory. Alteration not recommended.
DRAW_HEIGHT,DRAW_WID=200,1200 # The size of the drawing window for prompt mode, in pixels.
TEXT_HEIGHT,TEXT_WID=100,1000 # The size of the prompt display window, in pixels.
DRAW_COLOR=(255,255,255) # The color of the drawings and text.
DEBUGGING=False # Enables debug messages
# GCODE Generation Settings
Z_LIFT=1.5 # Height to lift writing device between each stroke.
START_GCODE=["G28\n",
            f"G01 Z{Z_LIFT} F500\n",
            f"G01 X0 Y20 (avoid clip)",
             "\n"]
END_GCODE=["G01 Z5 F500\n",
          f"G01 X0 Y{235/2} (avoid clips)",
           "G01 X0 Y235 (present page)\n"]

### AUTOMATICALLY DETERMINED CONSTANTS ###
PIX_PER_MM=SCREEN_RES_Y/SCREEN_HEIGHT # The number of pixels per mm on your screen

### FUNCTIONS ###
# Ensures that your user configs are set up properly.
def validate_configs():
    assert SCREEN_HEIGHT > 0, "Please measure your screen height and put it in config.py"
    assert (SCREEN_RES_X,SCREEN_RES_Y) != (-1,-1), "Please enter your screen resolution in config.py"
