# Walmart Financial Analysis

This project analyzes Walmart’s financial performance using real-world data from Financial Modeling Prep (FMP).

## Version 1 – Data Ingestion & Modeling Foundation
- Implemented a Python-based ingestion pipeline using the FMP stable API
- Secure API key handling via environment variables
- Ingests income statement, balance sheet, and cash flow data
- Stores raw financial data in JSON format
- Structured logging for ingestion activity
- Designed a star schema for financial statement analytics


## Environment Setup

This project uses conda environment for reproducibility.

```bash
conda env create -f environment.yml
conda activate walmart-financials




