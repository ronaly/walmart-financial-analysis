import json
from pathlib import Path
from datetime import datetime
import mysql.connector
from sqlalchemy import INT, VARCHAR
from config import MYSQL_CONFIG
from config import FACT_FIELD_MAPPING
from sql_statements import FACT_FINANCIALS_INSERT_SQL
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


#Map raw fact data fields to DB schema fields
def map_fact_record(raw_data:dict) -> dict:
    """
    Maps a raw FMP financial record to fact_financials fields.
    Missing fields default to None.
    """
    
    mapped_record = {}
    for raw_field, db_field in FACT_FIELD_MAPPING.items():
        mapped_record[db_field] = raw_data.get(raw_field)

    return mapped_record

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
        sql = FACT_FINANCIALS_INSERT_SQL
        

        for file in files:
            with open(file, 'r') as f:
                records = json.load(f)
                for r in records:
                    mapped = map_fact_record(r)
                    if not r.get("date"):
                        logger.warning(f"Skipping record with missing date in file {file.name}")
                        continue
                    period_type = "annual" if r.get("period") == "FY" else "quarterly"  
                    
                    cursor.execute(sql,(
                        company_id,
                        r.get("date"),
                        period_type,
                        mapped.get("revenue"),
                        mapped.get("cost_of_revenue"),
                        mapped.get("gross_profit"),
                        mapped.get("operating_expenses"),
                        mapped.get("operating_income"),
                        mapped.get("net_income"),
                        mapped.get("ebit"),   
                        mapped.get("ebitda"),
                        mapped.get("interest_expense"),
                        mapped.get("total_assets"),
                        mapped.get("total_liabilities"),
                        mapped.get("total_equity"),
                        mapped.get("current_assets"),
                        mapped.get("current_liabilities"),
                        mapped.get("cash_and_cash_equivalents"),
                        mapped.get("inventory"),
                        mapped.get("accounts_receivable"),
                        mapped.get("total_debt"),
                        mapped.get("operating_cash_flow"),
                        mapped.get("investing_cash_flow"),
                        mapped.get("financing_cash_flow"),
                        mapped.get("capital_expenditure"),
                        mapped.get("free_cash_flow")          
                    ))               
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