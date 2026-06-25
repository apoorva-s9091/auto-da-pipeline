import pandas as pd
import os
from utils.logger import logger

def load_data(file_path:str)-> pd.DataFrame:
    logger.info(f"Loading data from {file_path}")

    ext=os.path.splitext(file_path)[1].lower()

    if ext==".csv":
        df=pd.read_csv(file_path)
    elif ext in [".xls",".xlsx"]:
        df=pd.read_excel(file_path)
    elif ext==".json":
        df=pd.read_json(file_path )
    else:
        raise ValueError(f"unsupported file extension:{ext}")
    
    logger.info(f"data loaded successfully . Shape:{df.shape}")
    return df