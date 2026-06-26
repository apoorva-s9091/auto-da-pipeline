import pandas as pd
from utils.logger import logger

def validate(df:pd.DataFrame)->bool:
    logger.info("starting data validation")

    if df.empty:
        raise ValueError("Dataframe is empty")
    
    if len(df.columns)<2:
        raise ValueError("Dataframe has less than 2 columns")   
    
    if df.columns.duplicated().any():
        raise ValueError(f"Duplicate columns found: {df.columns[df.columns.duplicated().tolist()]}")
    
    null_pct= df.isnull().sum()/len(df)*100
    high_null_cols= null_pct[null_pct>20].index.tolist()
    if high_null_cols:
        logger.warning(f"high null percentage columns found:{high_null_cols}")


    dup_count= df.duplicated().sum()
    if dup_count>0:
        logger.warning(f"Duplicate rows found: {dup_count}")

    logger.info("validation completed successfully")
    return True