# main.py

from etl.etl_process import ETLProcess
from config.config import TAG_LINE, GAME_NAME_TANKTOP

# Run the ETL process
etl = ETLProcess(GAME_NAME_TANKTOP, TAG_LINE)
etl.run()

