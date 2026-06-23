import logging
import os
from datetime import datetime

LOG_DIR="logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename= os.path.join(LOG_DIR, f"pipeline_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger= logging.getLogger("auto-da-pipeline")