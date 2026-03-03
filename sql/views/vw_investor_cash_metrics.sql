DROP VIEW IF EXISTS vw_investor_cash_metrics;

CREATE VIEW vw_investor_cash_metrics AS
WITH raw_metrics AS (
    SELECT
        d.fiscal_year,
        f.operating_cash_flow,
        f.net_income,
        f.capital_expenditure,
        f.free_cash_flow,
        f.current_liabilities,
        f.revenue,
        f.cost_of_revenue,
        f.account_payables,
        f.accounts_receivable,
        f.inventory,
        -- Calculate Averages using LAG for the Time metrics
        (f.inventory + LAG(f.inventory) OVER (ORDER BY d.fiscal_year)) / 2 AS avg_inventory,
        (f.account_payables + LAG(f.account_payables) OVER (ORDER BY d.fiscal_year)) / 2 AS avg_ap,
        (f.accounts_receivable + LAG(f.accounts_receivable) OVER (ORDER BY d.fiscal_year)) / 2 AS avg_ar      
    FROM fact_financials f
    JOIN dim_date d  ON f.date_key = d.date_key
)
SELECT
    fiscal_year,
    operating_cash_flow AS cash,
    net_income AS profit,
    capital_expenditure,
    free_cash_flow,
    current_liabilities,
    revenue,
    cost_of_revenue,
    account_payables,
    accounts_receivable,
    inventory,

    -- CCR
    CASE 
        WHEN net_income = 0 OR net_income IS NULL THEN NULL
        ELSE operating_cash_flow / net_income
    END AS cash_conversion_ratio,

    -- DIO / DSO / DPO
    (avg_inventory / NULLIF(cost_of_revenue, 0)) * 365 AS DIO,
    (avg_ar / NULLIF(revenue, 0)) * 365 AS DSO,
    (avg_ap / NULLIF(cost_of_revenue, 0)) * 365 AS DPO,

    -- CCC
    ((avg_inventory / NULLIF(cost_of_revenue, 0)) * 365) + 
    ((avg_ar / NULLIF(revenue, 0)) * 365) - 
    ((avg_ap / NULLIF(cost_of_revenue, 0)) * 365) AS CCC
   

FROM raw_metrics;