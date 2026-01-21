import os
from dotenv import load_dotenv


load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/stable"

if not FMP_API_KEY:
    raise ValueError("FMP_API_KEY not found in environment variables.")

MYSQL_CONFIG = {
    'host': os.getenv("MYSQL_HOST"),
    'port': int(os.getenv("MYSQL_PORT")),
    'user': os.getenv("MYSQL_USER"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE")           
}

FACT_FIELD_MAPPING = {
    #Income Statement Fields
    "revenue": "revenue",
    "costOfRevenue": "cost_of_revenue",
    "grossProfit": "gross_profit",
    "operatingExpenses": "operating_expenses",     
    "operatingIncome": "operating_income",
    "netIncome": "net_income",
    "ebit": "ebit",
    "ebitda": "ebitda",
    "interestExpense": "interest_expense",
    #Balance Sheet Fields
    "totalAssets": "total_assets",
    "totalLiabilities": "total_liabilities",
    "totalEquity": "total_equity",
    "totalCurrentAssets": "current_assets",
    "totalCurrentLiabilities": "current_liabilities",
    "cashAndCashEquivalents": "cash_and_cash_equivalents",
    "inventory": "inventory",
    "accountsReceivables": "accounts_receivable",
    "totalDebt": "total_debt",
    #Cash Flow Statement Fields
    "operatingCashFlow": "operating_cash_flow",
    "investingCashFlow": "investing_cash_flow",
    "financingCashFlow": "financing_cash_flow",
    "capitalExpenditure": "capital_expenditure", 
    "freeCashFlow": "free_cash_flow"
}
