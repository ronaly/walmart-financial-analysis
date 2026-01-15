/*
Author: Ronaly Agdeppa
Date: Jan 15, 2026
Description: Seeding dim_company table with initial data.
*/


INSERT INTO dim_company (
    ticker,
    company_name,
    industry,
    sector,
    exchange,
    currency
)
VALUES (
    'WMT',
    'Walmart Inc.',
    'Discount Stores',
    'Consumer Defensive',
    'NASDAQ',
    'USD'   
)

ON DUPLICATE KEY UPDATE
    company_name = VALUES(company_name),
    industry = VALUES(industry),
    sector = VALUES(sector),
    exchange = VALUES(exchange),
    currency = VALUES(currency);    