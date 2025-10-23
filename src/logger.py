import logging
import os
from datetime import datetime

# -------- Step 1: Unique log file name তৈরি --------
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# -------- Step 2: logs ফোল্ডারের path তৈরি --------
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)  # না থাকলে ফোল্ডার তৈরি হবে

# -------- Step 3: Final log file path --------
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# -------- Step 4: Logging configuration --------
logging.basicConfig(
    filename=LOG_FILE_PATH,  # কোথায় log save হবে
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  
    level=logging.INFO,      # INFO level থেকে সব logs record করবে
)

