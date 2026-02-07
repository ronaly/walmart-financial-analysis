
# Walmart Financial Data Engineering & Analysis
> 🚧 **Status:** Visualization & insights in progress (Data engineering completed)

## Overview

This project demonstrates an end-to-end **data engineering and analytics workflow**, from API ingestion to analytics-ready data models, using publicly available financial data. The focus is on building a reliable ETL pipeline, designing a star schema for analytics, and enabling efficient financial analysis through SQL and visualization-ready outputs.

The project showcases practical skills in **Python, SQL, data modeling, and analytical thinking**, using real-world financial data.

---

## Objectives

* Extract public financial data via API
* Transform raw data into clean, structured formats
* Design a star schema optimized for financial analysis
* Enable efficient querying and downstream visualization (Tableau, dashboards)
* Demonstrate data engineering best practices in a realistic use case

---

## Data Source

Financial data is sourced from **Financial Modeling Prep (FMP)**, which provides licensed access to publicly available financial statements of publicly traded companies.

* Company: Walmart (public company)
* Data includes income statements, balance sheets, and cash flow statements
* Data is used strictly for **educational and portfolio demonstration purposes**

---

## Architecture & Workflow

1. **Extract**

   * Retrieved raw financial data via Financial Modeling Prep API using Python

2. **Transform**

   * Cleaned and standardized financial metrics
   * Normalized time-based and categorical fields
   * Prepared fact and dimension tables for analytics

3. **Load**

   * Loaded transformed data into MySQL database
   * Implemented a **star schema** with fact and dimension tables

4. **Analyze**

   * Validated data integrity using SQL
   * Enabled efficient financial queries and trend analysis
   * Prepared data for visualization tools such as Tableau

---

## Data Model

The project uses a **star schema** designed for financial analysis:

* **Fact table**

  * Financial metrics (revenue, net income, cash flow, etc.)

* **Dimension tables**

  * Company
  * Date (Fiscal Year, reporting period)
  

This structure supports scalable reporting, KPI analysis, and performance tracking.

---

## Tools & Technologies

* Python (ETL pipeline)
* SQL (data modeling, validation, analysis)
* Financial Modeling Prep API
* MySQL Database
* Tableau (for visualization and dashboards)

---

## Key Outcomes

* Built a reproducible ETL pipeline from API to analytics-ready tables
* Designed a clean star schema suitable for financial reporting
* Enabled fast and clear financial analysis through SQL queries
* Created a solid foundation for dashboards and executive-level insights
* Demonstrated a production-style workflow suitable for financial and operational analytics use cases

## Phase 1 - Data Engineering (DONE)
* ETL
* Star schema
* SQL validation

## Phase 2 - Visualization (In Progress)
* Tableau dashboards
* KPI views
* Financial trend analysis

## Phase 3 - Insights (Next)
* Executive Summary
* Key Findings
* Recommendations
* Business interpretation and implication






## Disclaimer

This project uses **publicly available financial data** sourced via Financial Modeling Prep.
It is intended **solely for educational and portfolio demonstration purposes**.

All company names, trademarks, and financial data belong to their respective owners.
This project is **not affiliated with or endorsed by Walmart**.

---

## Author

Developed as part of a personal data engineering and analytics portfolio to demonstrate real-world ETL, data modeling, and financial analysis skills.




## Environment Setup

This project uses conda environment for reproducibility.

```bash
conda env create -f environment.yml
conda activate wmt-financials




