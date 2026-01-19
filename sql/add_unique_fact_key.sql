/*
Author: Ronaly Agdeppa
Date: Jan 19, 2026
Description: Adding unique constraint to act as Security Gate to fact_financials table.
*/

-- --------------------------------------------------------
-- Adding a Security gate to fact_financials 
-- to prevent duplicate entries
-- --------------------------------------------------------
ALTER TABLE fact_financials
ADD UNIQUE KEY uq_fact (
    company_id,
    date_key,
    period_type
);