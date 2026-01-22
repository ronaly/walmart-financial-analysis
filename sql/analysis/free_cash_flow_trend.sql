/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: Is Walmart generating sustainable free cash flow?
*/

-- --------------------------------------------------------
-- Free Cash Flow Trend
-- Insigt Angle: Long-term sustainability /
--               Capacity for dividends, buybacks, expansion
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.operating_cash_flow,
    f.capital_expenditure,
    f.free_cash_flow
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
ORDER BY d.fiscal_year;
