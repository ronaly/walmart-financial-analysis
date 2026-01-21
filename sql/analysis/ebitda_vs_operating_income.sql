/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: How large is the gap between operating income and EBITDA?
*/

-- --------------------------------------------------------
-- EBITDA vs Operating Income
-- Insigt Angle: Depreciation Intensity /
---              Asset-heavy operations
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.operating_income,
    f.ebitda,
    f.ebitda - f.operating_income AS non_cash_adjustments
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.ebitda IS NOT NULL
ORDER BY d.fiscal_year;
