import json
from pathlib import Path
from datetime import datetime
import mysql.connector
from sqlalchemy import INT, VARCHAR
from config import MYSQL_CONFIG
from config import TABLE_CONFIG
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

###
### COMMENT: ON DUPLICATE KEY UPDATE  date_key = date_key clause is a do nothing strategy or ignore approach
###         to avoid inserting duplicate records based on the primary key (date_key) and avoid crashing.
###


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


#get the company_id from dim_company table
def get_company_id(ticker:str) -> int:
    """
    Enforcing data integrity by fetching company_id from dim_company table.
    Raises ValueError if ticker not found. Not allowing missing value. Let it fail loudly.
    """

    sql = "SELECT company_id FROM dim_company WHERE ticker = %s"
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (ticker,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(f"No Company ID found for ticker: {ticker}")
    except Exception as e:
        logger.error(f"Error fetching company_id for ticker {ticker}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def build_upsert_sql(table_name):
    table_conf = TABLE_CONFIG.get(table_name)

    keys = table_conf["keys"]
    mapping = table_conf["mapping"]

    fact_columns = list(mapping.values())
    all_columns = keys + fact_columns
    placeholders = ["%s"] * len(all_columns)

    update_clause = ",\n            ".join(f"{col}=COALESCE(VALUES({col}), {col})" for col in fact_columns)

    return f"""
        INSERT INTO {table_name} (
            {', '.join(all_columns)}
        )
        VALUES ({', '.join(placeholders)})
        ON DUPLICATE KEY UPDATE 
            {update_clause};
    """
 

def build_values(table_name, raw_record, key_values_dict):
    table_conf = TABLE_CONFIG[table_name]

    keys = table_conf["keys"]
    mapping = table_conf["mapping"]

    key_values = [key_values_dict[key] for key in keys]
    fact_values = [raw_record.get(raw_key) for raw_key in mapping.keys()]

    return tuple(key_values + fact_values)



#Insert raw data into fact_financials table
def load_fact_financials(ticker: str):    

    raw_dir = Path("data/raw")
    files = [
        file for file in raw_dir.glob(f"{ticker}_*.json")
        if any(x in file.name for x in ["income-statement", "balance-sheet-statement", "cash-flow-statement"])
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
    
        company_id = get_company_id(ticker)
        sql = build_upsert_sql("fact_financials")
        

        for file in files:
            with open(file, 'r') as f:
                records = json.load(f)
                for r in records:
                    
                    if not r.get("date"):
                        logger.warning(f"Skipping record with missing date in file {file.name}")
                        continue

                    key_data = {
                        "company_id": company_id,
                        "date_key": r.get("date"),
                        "period_type": "annual" if r.get("period") == "FY" else "quarterly" 
                    }
                    
                    values = build_values("fact_financials", r, key_data)
                    
                    cursor.execute(sql, values)

        conn.commit()   
        logger.info(f"Fact financials loaded for {ticker}.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading fact financials for {ticker}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
        



if __name__ == "__main__":
    #load_dim_date()
    load_fact_financials("WMT")
