import pandas as pd
from utils.logger import logger

def clean(df: pd.DataFrame)->pd.DataFrame:
    logger.info("Starting data cleaning")

    df= remove_duplicates(df)
    df= handle_nulls(df)
    choice= input("/nHandle outliers? (y/n): ").strip().lower()
    if choice.lower() == "y":
        df= handle_outliers(df)
    else:
        logger.info("Outlier handling skipped by user")
    df=encode_categorical(df) 

    logger.info("Data cleaning completed")
    return df

def remove_duplicates(df: pd.DataFrame)->pd.DataFrame:
    dup_count= df.duplicated().sum()
    if dup_count==0:
        logger.info("No duplicate rows found")
        return df
    print(f"\n found {dup_count} duplicate rows.")
    choice= input("Do you want to remove duplicate rows? (y/n): ").strip().lower()
    if choice=="y":
        df= df.drop_duplicates()
        logger.info(f"Removed {dup_count} duplicate rows")
    else:
        logger.info("Duplicate rows not removed by user")


    return df


def handle_nulls(df:pd.DataFrame)->pd.DataFrame:
    for col in df.columns:
        null_pct= df[col].isnull().sum()/len(df)*100
        if null_pct==0:
            continue
        
        print(f"\ncolumns '{col}' has {null_pct:.1f}% null values.")

        if df[col].dtype == "object":
            choice= input(f"Drop column or fill? (drop/fill) (y/n): ").strip().lower()
            if choice=="drop":
                df=df.drop(columns=[col])
                logger.warning(f"Dropped column '{col}' with {null_pct:.1f}% null values")
            else:
                df[col]=df[col].fillna(df[col].mode()[0])
                logger.info(f"Filled null values in column '{col}' with mode: {df[col].mode()[0]}")
        else:
            choice= input(f"fill with median, mode or drop? (drop/mean/median) (y/n): ").strip().lower()
            if choice=="drop":
                df=df.drop(columns=[col])
                logger.warning(f"Dropped column '{col}' with {null_pct:.1f}% null values")

            elif choice=="median":
                df[col]=df[col].fillna(df[col].median())
                logger.info(f"Filled null values in column '{col}' with median: {df[col].median()}")
            else:
                df[col]=df[col].fillna(df[col].mean())
                logger.info(f"Filled null values in column '{col}' with mean: {df[col].mean()}")
    
    return df

        
def handle_outliers(df:pd.DataFrame)->pd.DataFrame:
    numeric_cols= df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        logger.info("No numeric columns found for outlier handling")
        return df

    print(f"\nNumeric columns found: {numeric_cols}")
    choice= input("Do you want to handle outliers? (y/n): ").strip().lower()
    if choice!="y":
        logger.info("Outlier handling skipped by user")
        return df

    for col in numeric_cols:
        q1= df[col].quantile(0.25)
        q3= df[col].quantile(0.75)
        iqr= q3-q1
        lower_bound= q1-1.5*iqr
        upper_bound= q3+1.5*iqr

        outliers= df[(df[col]<lower_bound) | (df[col]>upper_bound)]
        outlier_count= len(outliers)

        if outlier_count==0:
            logger.info(f"No outliers found in column '{col}'")
            continue

        print(f"\nColumn '{col}' has {outlier_count} outliers.")
        choice= input("Do you want to remove or cap them? (remove/cap): ").strip().lower()
        if choice=="remove":
            df=df[~((df[col]<lower_bound) | (df[col]>upper_bound))]
            logger.warning(f"Removed {outlier_count} outliers from column '{col}'")
        else:
            df[col]=df[col].clip(lower=lower_bound, upper=upper_bound)
            logger.info(f"Capped outliers in column '{col}' to [{lower_bound}, {upper_bound}]")

    return df


def encode_categorical(df:pd.DataFrame)->pd.DataFrame:
    cat_cols= df.select_dtypes(include="object").columns.tolist()
    if not cat_cols:
        logger.info("No categorical columns found for encoding")
        return df

    print(f"\nCategorical columns found: {cat_cols}")
    choice= input("Do you want to encode categorical columns? (y/n): ").strip().lower()
    if choice!="y":
        logger.info("Categorical encoding skipped by user")
        return df

    for col in cat_cols:
        unique_vals= df[col].nunique()
        if unique_vals<=2:
            df[col]=df[col].map({df[col].unique()[0]:0, df[col].unique()[1]:1})
            logger.info(f"Binary encoded column '{col}'")
        else:
            dummies=pd.get_dummies(df[col], prefix=col, drop_first=True)
            df=pd.concat([df,dummies], axis=1)
            df=df.drop(columns=[col])
            logger.info(f"One-hot encoded column '{col}'")

    return df