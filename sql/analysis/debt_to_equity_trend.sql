/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: Is Walmart becoming more or less leveraged?
*/

-- --------------------------------------------------------
-- Debt & Capital Structure
-- Insigt Angle: Financial Risk /
--               Balance Sheet Strength
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.total_debt,
    f.total_equity,
    f.total_debt / f.total_equity AS debt_to_equity_ratio
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.total_equity IS NOT NULL
ORDER BY d.fiscal_year;
