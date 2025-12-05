# ✈️ Airline Flight Price Forecasting and Deployment on Azure

## 📌 Project Overview

This project builds a robust machine learning system to forecast and analyze airline flight prices, transforming raw API data into **actionable purchasing recommendations**.

The objectives achieved are:

  * Collect and process dynamic flight offers across IAH to LAX/ONT. ✅ Completed
  * Develop a **Time-Series Regression Model** to forecast fair market price. ✅ New\!
  * Implement a **Deal Detection Engine** to generate buy/wait recommendations. ✅ New\!
  * Develop automated data pipelines and dashboards using Azure. ⏳ In Progress

This project highlights end-to-end skills in **API integration, data engineering, time-series modeling, MLOps preparation, and cloud deployment**.

-----

## 🗂️ Project Structure

The project structure is updated to reflect the consolidation of all modeling logic into a single deployment-ready Python script.

```text
airline-flight-prices/
|
├── notebooks/
│   └── 1_data_collection.ipynb ✅ Completed
│   └── 2_data_cleaning.ipynb ✅ Completed
│   └── 3_EDA.ipynb ✅ Completed
│   └── 4_Flight_Price_Forecasting.ipynb 🚀 Logic Migrated to scripts/
│
├── data/
│   └── raw/
│   └── clean/
├── scripts/
│   └── scripts.py 
│   └── models.py Upcoming -> will contains entire ML pipeline (Steps 1-8) 
├── models/
│   └── flight_price_model_v3.pkl 🆕 Trained & Serialized Model
├── figures/
├── README.md
└── requirements.txt
```

-----

## ✅ Completed Work

### Data Collection & Cleaning

<img width="3999" height="2599" alt="image" src="https://github.com/user-attachments/assets/f32a1f5e-2b9d-4209-8ab9-5662d2868bb3" />


  * Connected to Amadeus API and pulled flight offers for IAH → LAX/ONT.
  * Standardized data, handled missing values, and consolidated segments into unique journey rows.

### Exploratory Data Analysis (EDA)

  * Analyzed price distributions, trends over time, and airline-specific patterns.
  * Extracted actionable insights (best day to search, fly, and optimal booking window).

### Machine Learning Forecasting (Phase 2 Complete) 🧠

| Component | Detail | Impact |
| :--- | :--- | :--- |
| **Feature Engineering** | Created time-series features: **Price Lag, Rolling Mean, and Volatility**. | Critical for predicting dynamic price changes and momentum. |
| **Model** | **LightGBM Regressor** trained using **Time Series Cross-Validation (TSCV)**. | Ensures the model generalizes robustly to future, unseen data. |
| **Performance** | Model evaluated using MAE, RMSE, and **MAPE** (Mean Absolute Percentage Error). | MAPE provides a clear, interpretable measure of forecast accuracy. |
| **Deal Detection** | Implemented logic to categorize offers as **'EXCELLENT'**, **'GOOD'**, **'FAIR'**, or **'OVERPRICED'**. | Generates the final, actionable recommendation (**"🔥 BUY NOW"**). |
| **Persistence** | The trained model is serialized (`flight_price_model_v3.pkl`) and ready for deployment. | Allows for fast, efficient loading for inference. |

-----

## 🚀 Roadmap (Next Steps)

### Phase 3 – Azure Integration & Deployment ☁️

This phase focuses entirely on transforming the local pipeline into a scalable, automated cloud solution using Azure's MLOps capabilities.

[Image of machine learning deployment pipeline]

  * **Model Registration:** Register the `flight_price_model_v3.pkl` model within **Azure Machine Learning Service**.
  * **Data Pipeline Automation:** Use **Azure Data Factory** (ADF) to orchestrate daily data collection from the API and preprocessing into **Azure Blob Storage**.
  * **Real-time Inference API:** Deploy the model via **Azure Container Instances (ACI)** or **Azure Kubernetes Service (AKS)** to create a low-latency scoring API.
  * **Monitoring & Visualization:** Integrate the predicted data and deal categories into **Power BI** for ongoing performance monitoring and business user dashboards.

-----

## 📊 Tools & Tech Stack

  * **Modeling**: `Python`, `pandas`, `numpy`, `scikit-learn`, **`lightgbm`**
  * **APIs**: Amadeus API
  * **Cloud (Focus)**: **Azure Blob Storage, Azure Data Factory, Azure ML, Azure Functions/ACI/AKS, Azure Power BI**

-----

## 🔑 Key Value

This project demonstrates proficiency across the entire data science lifecycle:

  * End-to-end data engineering and API data wrangling.
  * Advanced **time-series feature engineering** and robust **model validation (TSCV)**.
  * Translating model output into **actionable business intelligence** (Deal Alerts).
  * Preparation of a production-ready model artifact for **Cloud Deployment (MLOps)**.
