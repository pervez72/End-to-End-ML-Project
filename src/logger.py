import logging
import os
from datetime import datetime

# -------- Step 1: Unique log file name তৈরি --------
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# -------- Step 2: logs ফোল্ডারের path তৈরি --------
logs_path = os.path.join(os.getcwd(), "logs")  # current working directory + logs folder
os.makedirs(logs_path, exist_ok=True)          # না থাকলে ফোল্ডার তৈরি হবে

# -------- Step 3: Final log file path --------
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# -------- Step 4: Logging configuration --------
logging.basicConfig(
    filename=LOG_FILE_PATH,  # কোথায় log save হবে
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,      # INFO level থেকে সব logs record করবে (INFO, WARNING, ERROR, CRITICAL)
)

# -------- Step 5: Console log enable (optional but useful) --------
# এতে করে log message শুধু file-এ না, console-এও দেখা যাবে
console_handler = logging.StreamHandler()
console_format = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)
logging.getLogger().addHandler(console_handler)

# -------- Step 6: Test message --------
if __name__ == "__main__":
    logging.info("Logger file is working properly ✅")
    logging.warning("This is a sample warning message ⚠️")
    logging.error("This is a sample error message ❌")

