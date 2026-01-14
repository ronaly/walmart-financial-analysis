/*
Author: Ronaly Agdeppa
Date: Jan 14, 2026
Description: SQL schema file for Financial Modeling Prep (FMP) data.
*/

-- CLEAN SLATE: Drop tables if they exist
DROP TABLE IF EXISTS fact_financials;
DROP TABLE IF EXISTS dim_company;
DROP TABLE IF EXISTS dim_date;


-- --------------------------------------------------------
-- 1. DIMENSION: COMPANY
-- Stores the qualitative/static info
-- --------------------------------------------------------

CREATE TABLE dim_company (
    company_id INT AUTO_INCREMENT PRIMARY KEY,  -- Auto-incrementing ID
    ticker VARCHAR(10) UNIQUE NOT NULL,   -- WMT for Walmart
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(255),
    sector VARCHAR(255),
    exchange VARCHAR(50),   -- NASDAQ
    currency VARCHAR(10)
);


-- --------------------------------------------------------
-- 2. DIMENSION: DATE
-- Slice data by years and quarters
-- --------------------------------------------------------
CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    fiscal_year INT,
    fiscal_year_label VARCHAR(10),  -- e.g., FY2025
    fiscal_quarter VARCHAR(2),  -- Q1, Q2, Q3, Q4
    calendar_year INT
);

-- --------------------------------------------------------
-- 3. FACT: FINANCIALS
-- Stores the quantitative/numerical data
-- --------------------------------------------------------
CREATE TABLE fact_financials (
    fact_id BIGINT AUTO_INCREMENT PRIMARY KEY,    -- Auto-incrementing ID
    company_id INT NOT NULL, -- Links to dim_company
    date_key DATE NOT NULL,       -- Links to dim_date
    period_type ENUM('annual', 'quarterly') NOT NULL,  -- e.g., annual, quarterly
    
    -- Income Statement Metrics
    revenue NUMERIC(20, 2),        -- (20,2) allows for trillions of dollars
    cost_of_revenue NUMERIC(20, 2),
    gross_profit NUMERIC(20, 2),
    operating_income NUMERIC(20, 2),
    ebit NUMERIC(20, 2),
    net_income NUMERIC(20, 2),
    interest_expense NUMERIC(20, 2),
    
    -- Balance Sheet Metrics
    total_assets NUMERIC(20, 2),
    total_liabilities NUMERIC(20, 2),
    total_equity NUMERIC(20, 2),
    current_assets NUMERIC(20, 2),
    current_liabilities NUMERIC(20, 2),
    cash_and_cash_equivalents NUMERIC(20, 2),
    inventory NUMERIC(20, 2),
    accounts_receivable NUMERIC(20, 2),
    total_debt NUMERIC(20, 2),
    
    -- Cash Flow Metrics
    operating_cash_flow NUMERIC(20, 2),
    capital_expenditure NUMERIC(20, 2),
    free_cash_flow NUMERIC(20, 2),

    FOREIGN KEY (company_id) REFERENCES dim_company(company_id),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);