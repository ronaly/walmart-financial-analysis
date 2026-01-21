# Walmart Financial Analysis

This project analyzes Walmart’s financial performance using real-world data from Financial Modeling Prep (FMP).


## Version 1 – Data Ingestion, Modeling & Loading Foundation

* Implemented an end-to-end Python-based ETL pipeline using the Financial Modeling Prep (FMP) stable API
* Secure API key and database credential handling via environment variables
* Ingests income statement, balance sheet, and cash flow data from the FMP API
* Stores raw financial data in JSON format for traceability and reprocessing
* Designed and implemented a star schema for financial statement analytics

  * `dim_company` for company metadata
  * `dim_date` for fiscal and calendar time dimensions
  * `fact_financials` for consolidated financial metrics
* Loaded dimension and fact tables into MySQL using idempotent upsert logic
* Enforced fact table grain using a composite unique key
* Prevented data loss during multi-statement loads using `COALESCE`-based upserts
* Implemented structured logging for ingestion, loading, and error handling
* Supports safe re-runs and incremental enrichment of financial data



## Environment Setup

This project uses conda environment for reproducibility.

```bash
conda env create -f environment.yml
conda activate walmart-financials




