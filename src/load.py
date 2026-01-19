import json
from pathlib import Path
from datetime import datetime
import mysql.connector
from sqlalchemy import INT, VARCHAR
from config import MYSQL_CONFIG
from logger import setup_logger

logger = setup_logger("load_logger", "load.log")

#DB connection helper
def get_db_connection():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        logger.info("Database connection established.")
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to database: {err}")
        raise


#Extract unique dates from raw JSON files
def extract_unique_dates() -> list:
    raw_dir = Path("data/raw")
    date_records = {}

    for file in raw_dir.glob("*.json"):
        try:
            with open(file, 'r') as f:
                records = json.load(f)
                for r in records:
                    date_str = r.get("date")
                    if not date_str:
                        continue

                    if date_str not in date_records:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                        calendar_year = date_obj.year
                        fiscal_year = int(r.get("fiscalYear"))
                        period = r.get("period")
                        fiscal_quarter = None

                        date_records[date_str] = {
                            "date_key": date_obj,
                            "fiscal_year": fiscal_year,
                            "fiscal_year_label": f"FY{fiscal_year}",
                            "fiscal_quarter": fiscal_quarter,
                            "calendar_year": calendar_year
                        }
            logger.info(f"Extracted dates from {file.name}")
        except Exception as e:
            logger.error(f"Error reading {file.name}: {e}")

    return list(date_records.values())


#Insert into dim_date table
def load_dim_date():

    records = extract_unique_dates()

    if not records:
        logger.warning("No date records found to load.")
        return


    sql = """
    INSERT INTO dim_date (
        date_key,
        fiscal_year,
        fiscal_year_label,
        fiscal_quarter,
        calendar_year
    )
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        date_key=date_key;
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        for r in records:
            cursor.execute(sql, (
                r["date_key"],
                r["fiscal_year"],
                r["fiscal_year_label"],
                r["fiscal_quarter"],
                r["calendar_year"]
            ))
        conn.commit()
        logger.info("Inserted %d rows into dim_date.", len(records))
    
    except Exception as e:
        conn.rollback()
        logger.error(f"Error inserting records into dim_date: {e}")
    
    finally:
        cursor.close()
        conn.close()
        logger.info("Database connection closed.")  



if __name__ == "__main__":
    load_dim_date()