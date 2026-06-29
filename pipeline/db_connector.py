import pandas as pd
from utils.logger import logger

def load_from_db(connection_string: str, query: str) -> pd.DataFrame:
    try:
        from sqlalchemy import create_engine
        logger.info(f"Connecting to database...")
        engine = create_engine(connection_string)
        df = pd.read_sql(query, engine)
        logger.info(f"Data loaded from database. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

def get_db_input() -> tuple:
    print("\nDatabase Connection")
    print("Examples:")
    print("  MySQL:      mysql+pymysql://user:password@host/dbname")
    print("  PostgreSQL: postgresql://user:password@host/dbname")
    print("  SQLite:     sqlite:///path/to/file.db")
    
    connection_string = input("\nEnter connection string: ").strip()
    query = input("Enter SQL query: ").strip()
    
    return connection_string, query