# main.py

from etl.etl_process import ETLProcess
from config.config import TAG_LINE, GAME_NAME_TANKTOP, GAME_NAME_VELBRI, GAME_NAME_CAMACHBRO, GAME_NAME_KINGVEI

# List of game names
game_names = [GAME_NAME_TANKTOP, GAME_NAME_VELBRI, GAME_NAME_CAMACHBRO, GAME_NAME_KINGVEI]

# Run the ETL process
etl = ETLProcess(game_names, TAG_LINE)
etl.run()

