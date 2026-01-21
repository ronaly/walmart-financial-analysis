/*
Author: Ronaly Agdeppa
Date: Jan 20, 2026
Description: Adding new columns to fact_financials for metric expansion.
*/

-- --------------------------------------------------------
-- Adding new columns to fact_financials 
-- for metric expansion
-- --------------------------------------------------------

ALTER TABLE fact_financials
ADD COLUMN operating_expenses DECIMAL(20,4),
ADD COLUMN ebitda DECIMAL(20,4),
ADD COLUMN investing_cash_flow DECIMAL(20,4),
ADD COLUMN financing_cash_flow DECIMAL(20,4);