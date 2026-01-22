/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: Is Walmart growing, and is profit keeping pace?
*/

-- --------------------------------------------------------
-- Revenue & Net Income Trend
-- Insight Angle: Growth consistency / 
--                Revenue vs Profitability divergence
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.revenue,
    f.net_income
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
ORDER BY d.fiscal_year;
