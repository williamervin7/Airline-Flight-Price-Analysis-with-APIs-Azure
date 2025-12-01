# ✈️ Airline Flight Price Analysis with APIs & Azure

## 📌 Project Overview

This project forecasts and analyzes airline flight prices using real-time data from the Amadeus API.
The objectives were to:

* Collect and process dynamic flight offers across IAH to LAX and dates. ✅ Completed
* Explore business-relevant questions around pricing and booking behavior. ✅ Completed
* Develop automated data pipelines and dashboards using Azure.

This project highlights skills in **API integration, data engineering, statistical analysis, EDA, and cloud deployment**.

---

## 🗂️ Project Structure

```text
airline-flight-prices/
|
├── notebooks/
│   └── 1_data_collection.ipynb ✅ Completed
│   └── 2_data_cleaning.ipynb ✅ Completed
│   └── 3_EDA.ipynb ✅ Completed
│   └── 4_Flight_Price_Forecasting.ipynb
│
├── data/
│   └── raw/
│   └── clean/
├── scripts/
│   └── scripts.py
|   └── models.py
├── figures/
├── README.md
└── requirements.txt
```

---

## ✅ Completed Work

### Data Collection

* Connected to Amadeus API and pulled flight offers for IAH → LAX (11/15/2025–12/31/2025).
* Stored raw CSV data in a reproducible format.

### Data Cleaning

* Standardized columns, handled missing values, and converted date/time fields.
* Created derived features like `days_until_departure`, `is_weekend`, and day/week indicators.

### Exploratory Data Analysis (EDA)

* Examined dataset shape, column types, missing values, and basic statistics.
* Analyzed price distributions, trends over time, and airline-specific patterns.
* Visualized relationships between price, booking timing, day of week, and flight characteristics.
* Extracted actionable insights (best day to search, fly, and optimal booking window).

---

## 🚀 Roadmap (Next Steps)

### Phase 2 – Local Modeling & Price Alerts

* Develop and test predictive models locally using the cleaned dataset.
* Explore regression and time-series approaches to forecast flight prices.
* Implement a basic price alert system based on model predictions or thresholds.
* Validate models and alerts to ensure reliability before scaling to Azure.
* Prepare scripts and workflows for seamless migration to cloud deployment.

### Phase 3 – Azure Integration

* Deploy automated pipeline: **API → Azure Blob Storage → Azure Data Factory → Azure ML / Power BI**.
* Daily refresh of flight data.
* (Optional) Real-time price alerts.

---

## 📊 Tools & Tech Stack

* **Python**: `requests`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`
* **APIs**: Amadeus API
* **Cloud**: Azure Blob Storage, Azure Data Factory, Azure ML, Azure Power BI

---

## 🔑 Key Value

This project demonstrates:

* API data wrangling and automation
* Business-focused analysis with actionable insights
* Cloud pipeline deployment with Azure


---

If you want, I can also rewrite your **Project Overview** section in 3–4 punchy sentences that reads more like a portfolio description rather than a roadmap — which often looks cleaner on GitHub. Do you want me to do that?
