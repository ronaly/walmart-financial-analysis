/*
Author: Ronaly Agdeppa
Date: Jan 21, 2026
Question: Is Walmart becoming more or less profitable?
*/

-- --------------------------------------------------------
-- Profitability Margins Analysis
-- Insigt Angle: Margin compression or expansion /
--               Cost control effectiveness
-- --------------------------------------------------------
SELECT
    d.fiscal_year,
    f.net_income / f.revenue AS net_margin,
    f.operating_income / f.revenue AS operating_margin
FROM fact_financials f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.revenue IS NOT NULL
ORDER BY d.fiscal_year;
