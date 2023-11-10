''' config for handwriting-data
* Contains user dependent constants
* Contains other configurable program settings
'''

# by default, screen height is -1, and resolution is -1,-1. Please change these values.

# User configured constants. Used to calculate pixels per millimeter value.
SCREEN_HEIGHT=195 # The height of your screen, in millimeters.
SCREEN_RES_X,SCREEN_RES_Y=1920,1080 # The resolution of your screen (ex., 1920x1080 becomes 1920,1080)

# Other settings
PROMPTS_DIR="prompts/writing_prompts.txt" # The path to the prompts you wish to gather data on.
PROMPT_DATA_DIR="prompts/prompt_data/" # Data directory. Alteration not recommended.
DRAW_HEIGHT,DRAW_WID=200,1200 # The size of the drawing window for prompt mode, in pixels.
TEXT_HEIGHT,TEXT_WID=100,1000 # The size of the prompt display window, in pixels.
DRAW_COLOR=(255,255,255) # The color of the drawings and text.
DEBUGGING=False # Enables debug messages

# Automatically determined constants
PIX_PER_MM=SCREEN_RES_Y/SCREEN_HEIGHT # The number of pixels per mm on your screen

# Ensures that your user configs are set.
def validate_configs():
    assert SCREEN_HEIGHT > 0, "Please measure your screen height and put it in config.py"
    assert (SCREEN_RES_X,SCREEN_RES_Y) != (-1,-1), "Please enter your screen resolution in config.py"