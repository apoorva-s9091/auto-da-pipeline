import pandas as pd
import io
from utils.logger import logger

def profile(df:pd.DataFrame)->dict:
    logger.info("Starting data profiling")

    profile_result={
        "shape":df.shape,
        "columns":df.columns.tolist(),
        "dtypes":df.dtypes.astype(str).to_dict(),
        "null_counts":df.isnull().sum().to_dict(),
        "null_percentage":(df.isnull().sum()/len(df)*100).round(2).to_dict(),
        "numeric_summary":df.describe().to_dict(),
        "categorical_summary":df.select_dtypes(include="object").columns.tolist(),
        "numeric_cols":df.select_dtypes(include="number").columns.tolist(),
    }

    profile_result["info"] = get_info(df)

    return profile_result

def get_info(df:pd.DataFrame)->str:
    buffer=io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()