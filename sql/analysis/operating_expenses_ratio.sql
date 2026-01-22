/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: Are operating expenses growing faster than revenue?
*/

-- --------------------------------------------------------
-- Operating Expenses vs Revenue
-- Insigt Angle: Operation Efficiency /
--               Scale benefits (or lack thereof)
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.operating_expenses,
    f.revenue,
    f.operating_expenses / f.revenue AS opex_ratio
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.operating_expenses IS NOT NULL
ORDER BY d.fiscal_year;
