# ✈️ Airline Flight Price Analysis with APIs & Azure

## 📌 Project Overview
This project explores airline flight pricing using live data from Amadeus APIs.  
The goal is to demonstrate how to:
- Pull and process dynamic API data.
- Answer business-relevant questions about flight prices and booking behavior.
- Build scalable pipelines with Azure for automation and dashboards.

This project highlights skills in **API integration, exploratory data analysis, statistical reasoning, dashboarding, and cloud deployment**.
---
## 🗂️ Project Structure

```airline-flight-prices/
|
├── notebooks/ # Jupyter/Colab notebooks
│ └── 1_data_collection.ipynb
│ └── 2_exploratory_analysis.ipynb
│ └── 3_business_questions.ipynb
│
├── data/ # Local cache of pulled data (excluded via .gitignore)
|└── raw
├── scripts/ # Python scripts for API calls, cleaning
|└── scripts.py
├── figures/ # Visualizations for README and reports
├── README.md # Project outline
└── requirements.txt # Dependencies 
```
---

## 🚀 Roadmap

### Phase 1 (Local: Python + Colab)
- Connect to Skyscanner / Amadeus API.
- Collect flight pricing data (routes, times, booking windows).
- Explore key trends: cheapest times to fly, seasonal effects, route comparisons.
- Answer structured business questions:
  - *What’s the average price swing for Houston → NYC by booking month?*
  - *Which routes have the highest seasonal variation?*
  - *What is the optimal booking window to minimize costs?*
  - *How do weekend vs. weekday departures affect average price?*

### Phase 2 
- Build an interactive dashboard (Streamlit, Dash, or Power BI).
- Visualize trends: booking strategies, cost comparisons, route insights.
- Package notebooks and scripts into a clean, reproducible workflow.

### Phase 3 (Azure Integration)
- Deploy a pipeline: **API → Azure Blob Storage → Azure Data Factory → Azure ML/Power BI**.
- Automate daily refresh of flight data.
- (Bonus) Implement real-time alerts (e.g., notify when flights drop below $300).

---

## 📊 Tools & Tech Stack
- **Python**: `requests`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`
- **APIs**: Skyscanner API, Amadeus API (depending on access)
- **Dashboards**: Streamlit / Plotly Dash / Power BI
- **Cloud**: Azure Blob Storage, Azure Data Factory, Azure ML, Azure Power BI

---

## 📈 Future Enhancements
- Flight price prediction models (time series / regression).
- Anomaly detection (unexpected price drops or spikes).
- ML-based recommender system for best travel options.
- Scaling to multiple routes and real-time streaming.

---

## 🔑 Key Value
This project demonstrates:
- API data wrangling and automation.
- Business-focused analysis with actionable insights.
- Cloud pipeline deployment with Azure.
- Dashboarding and communication of results.
