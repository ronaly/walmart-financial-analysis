/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: Are reported profits backed by real cash?
*/

-- --------------------------------------------------------
-- Cash Flow Quality
-- Insigt Angle: Earning quality /
--              Red flags in accounting vs cash
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.operating_cash_flow,
    f.net_income,
    f.operating_cash_flow / f.net_income AS cash_conversion_ratio
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.net_income <> 0
ORDER BY d.fiscal_year;
