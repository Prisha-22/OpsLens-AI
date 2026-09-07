# 🚚 OpsLens AI — Delivery Operations Intelligence Platform

> **An end-to-end data analytics and AI-powered operations intelligence platform for monitoring, predicting, and improving delivery performance.**

OpsLens AI transforms delivery data into actionable operational intelligence through **analytics, KPI monitoring, anomaly detection, root-cause analysis, forecasting, machine-learning prediction, and automated recommendations**.

The platform is designed around a real-world food-delivery operations scenario similar to platforms such as Zomato and Swiggy.

---

## 🎯 Project Overview

Modern delivery platforms generate large volumes of operational data involving:

* Delivery times
* Rider performance
* Traffic conditions
* Weather
* Delivery distance
* Vehicle conditions
* Multiple-order assignments
* Peak-hour demand
* City/zone performance

Simply reporting these metrics is not enough.

**OpsLens AI answers the next-level operational questions:**

* Why are deliveries becoming slower?
* Which operational factors have the biggest impact?
* Which deliveries are anomalous?
* Which cities or operating conditions are high-risk?
* What delivery time should we expect?
* Where should operations teams intervene?
* What actions can reduce delivery delays?

The platform combines **descriptive analytics + diagnostic analytics + predictive ML + operational recommendations** into a single application.

---

## 📊 Real Dataset

The project uses a cleaned **Zomato-style real delivery dataset** containing:

* **45,584 delivery records**
* **24 operational features**
* Delivery time
* Distance
* Rider information
* Weather
* Traffic
* Vehicle condition
* Order type
* Vehicle type
* Multiple deliveries
* Festival information
* City
* Peak-hour indicators
* Weekend indicators

### Data Quality

The dataset was validated before analytics and ML processing.

| Metric                |    Result |
| --------------------- | --------: |
| Total Records         |    45,584 |
| Duplicate Order IDs   |         0 |
| Missing Order IDs     |         0 |
| Missing Delivery Time |         0 |
| Missing Distance      |         0 |
| Missing Weather       |         0 |
| Missing Traffic       |         0 |
| Missing City          |         0 |
| Average Delivery Time | 26.29 min |
| Average Distance      |   9.73 km |
| Maximum Distance      |  20.97 km |

---

# 🧠 Core Capabilities

## 1. Executive Operations Dashboard

The main dashboard provides a high-level operational view with:

* Average delivery time
* Operational health score
* Anomaly count
* Strongest operational factor
* Risk level
* Traffic impact
* Peak-hour impact
* Multiple-delivery impact
* Vehicle-condition impact
* Long-distance delivery impact
* AI-generated recommendations

### Current Operational Snapshot

| KPI                   |     Value |
| --------------------- | --------: |
| Total Deliveries      |    45,584 |
| Average Delivery Time | 26.29 min |
| Operational Health    |  40 / 100 |
| Risk Level            |      High |
| Detected Anomalies    |     2,280 |
| Anomaly Rate          |     ~5.0% |

---

# 🔎 2. Root Cause Analysis

OpsLens AI identifies the operational factors contributing to longer delivery times.

### Key Findings

| Factor                 |     Impact |
| ---------------------- | ---------: |
| Multiple Deliveries    | +15.29 min |
| Jam Traffic            |  +4.88 min |
| Poor Vehicle Condition |  +3.78 min |
| Very Long Distance     |  +3.49 min |
| Peak Hour              |  +2.37 min |

The system also evaluates city-level operational performance.

**Semi-Urban deliveries average approximately 49.73 minutes**, making the city segment a major operational risk.

---

# 🚨 3. Anomaly Detection

The anomaly detection module identifies deliveries that behave differently from normal operational patterns.

### Current Results

* Total deliveries analyzed: **45,584**
* Detected anomalies: **2,280**
* Anomaly rate: **~5.0%**

The system considers operational characteristics such as:

* Delivery duration
* Distance
* Traffic
* Weather
* Rider characteristics
* Vehicle condition
* Multiple deliveries
* Peak-hour conditions

This allows operations teams to focus on unusual deliveries instead of manually inspecting the entire dataset.

---

# 📈 4. Delivery Forecasting

OpsLens AI includes a delivery-time forecasting module to estimate upcoming operational performance.

Because the available dataset does not contain a reliable continuous timestamp series, the forecasting module groups sequential records into operational periods rather than pretending the data represents actual calendar days.

### Forecast Output

The system generates a **7-period delivery-time forecast** based on historical operational patterns.

This can be used to monitor whether average delivery performance is expected to:

* Increase
* Decrease
* Remain stable

---

# 🤖 5. ML Delivery-Time Prediction

OpsLens AI includes a machine-learning prediction pipeline for estimating delivery duration for a new order.

### Model

**Random Forest Regressor**

### Input Features

* Distance
* Rider age
* Rider rating
* Weather
* Traffic level
* Vehicle condition
* Order type
* Vehicle type
* Multiple deliveries
* Festival
* City
* Pickup hour
* Peak hour
* Weekend

Categorical variables are handled using **OneHotEncoder**, while numerical features are passed through the preprocessing pipeline.

### Example

Given operational conditions for a new delivery, the system produces:

* Predicted delivery time
* Risk classification
* Major contributing factors
* Suggested intervention

---

# 💡 6. AI Operational Insights

The AI Insights module converts analytical findings into business-friendly explanations.

Instead of presenting only numbers, the system generates insights around:

* Delivery performance
* Traffic
* Peak hours
* Multiple deliveries
* Vehicle conditions
* Distance
* City-level performance

This bridges the gap between **data analysis and business decision-making**.

---

# 🛠️ 7. Automated Recommendations

OpsLens AI converts root-cause findings into operational actions.

### Example Recommendations

**Critical — Multiple Deliveries**

Multiple-order assignments significantly increase delivery time.

**Recommended action:**
Limit multi-order assignments during high-demand periods and apply stricter distance thresholds for order batching.

---

**High — Traffic**

Jam traffic increases delivery time by approximately **4.88 minutes**.

**Recommended action:**
Increase rider availability during heavy traffic periods and prioritize nearby orders in congested zones.

---

**High — Peak Hour**

Peak-hour deliveries take approximately **2.37 minutes longer**.

**Recommended action:**
Deploy additional riders during peak hours and dynamically balance order assignments.

---

**High — Vehicle Condition**

Poor vehicle condition is associated with approximately **3.78 additional minutes**.

**Recommended action:**
Introduce regular vehicle inspections and prioritize maintenance for riders with poor vehicle-condition scores.

---

# 📊 Analytics Module

The Analytics page provides interactive analysis across:

### Delivery Performance

* Average delivery time
* Median delivery time
* Delivery distance
* Delivery-time distributions

### Environment

* Traffic
* Weather
* Peak-hour conditions

### Operations

* Multiple deliveries
* Vehicle conditions
* Order types
* Weekend vs weekday patterns

### Rider Performance

* Rider age
* Rider rating
* Vehicle type

### Geography

* City-level delivery performance

Interactive filters allow users to analyze specific operational segments.

---

# 🖥️ Streamlit Application

The project is delivered through an interactive Streamlit application with eight major modules:

| Page                   | Purpose                              |
| ---------------------- | ------------------------------------ |
| 🏠 Executive Dashboard | Overall operational health           |
| 🧠 AI Insights         | Automated business insights          |
| 🔍 Analytics           | Interactive operational analysis     |
| 🚨 Anomalies           | Detect unusual deliveries            |
| 📈 Forecast            | Forecast future delivery performance |
| 🤖 Prediction          | Predict delivery time                |
| 💡 Recommendations     | Generate operational actions         |
| 🔎 Root Cause          | Identify delay drivers               |

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   Zomato Delivery    │
                    │       Dataset        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Cleaning &       │
                    │ Validation            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │   Delivery Database  │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐   ┌─────────────┐
        │ Analytics │    │ ML Models  │   │ AI Insights │
        └─────┬─────┘    └─────┬─────┘   └──────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │     Streamlit        │
                    │     Application      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Operational Decisions │
                    │ & Recommendations     │
                    └──────────────────────┘
```

---

# 🧰 Tech Stack

### Programming

* Python
* SQL

### Data & Database

* Pandas
* NumPy
* PostgreSQL

### Machine Learning

* Scikit-learn
* Random Forest
* One-Hot Encoding
* Feature preprocessing
* Anomaly detection
* Forecasting

### Visualization

* Plotly
* Matplotlib

### Application

* Streamlit

### Development

* Git
* GitHub
* VS Code

---

# 📁 Project Structure

```text
OpsLens-AI/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   └── real_data/
│       └── Zomato Dataset.csv
│
├── docs/
│   ├── 01_Project_Overview.md
│   ├── 02_Business_Requirements.md
│   ├── 03_KPIs.md
│   ├── 04_Dataset_Design.md
│   ├── 05_SQL_Plan.md
│   ├── 06_Python_Plan.md
│   ├── 07_Business_Process.md
│   └── 08_Database_Architecture.md
│
├── python/
│   ├── analytics/
│   ├── ingestion/
│   ├── insights/
│   ├── ml/
│   ├── visualizations/
│   ├── database.py
│   └── main.py
│
├── sql/
│   ├── 01_Basic_SQL/
│   ├── 02_Business_KPIs/
│   ├── 03_Advanced_SQL/
│   ├── create_tables.sql
│   └── README.md
│
├── streamlit/
│   ├── components/
│   ├── pages/
│   └── app.py
│
├── reports/
├── images/
├── notebooks/
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/Prisha-22/OpsLens-AI.git
cd OpsLens-AI
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure PostgreSQL

Create a PostgreSQL database and configure the database connection according to the project's configuration files.

> Never commit database passwords, API keys, or other secrets to GitHub.

## 5. Run the application

From the project root:

```bash
python -m streamlit run streamlit/app.py
```

The application will open in your browser.

---

# 📌 Key Business Insights

The current dataset analysis shows several important operational patterns:

### 🚦 Traffic

Jam traffic increases average delivery time by approximately **4.88 minutes**.

### 🌙 Peak Hours

Peak-hour deliveries take approximately **2.37 minutes longer** than non-peak deliveries.

### 📦 Multiple Deliveries

Multiple-order assignments have one of the strongest operational impacts, increasing delivery time substantially.

### 🚗 Vehicle Condition

Poor vehicle condition is associated with approximately **3.78 additional minutes**.

### 📍 Distance

Very long-distance deliveries take approximately **3.49 minutes longer**.

### 🏙️ City Operations

Semi-Urban deliveries show significantly higher delivery times and represent a major operational risk area.

---

# 🎯 Project Goals

OpsLens AI was designed to demonstrate an end-to-end analytics workflow:

```text
Raw Data
   ↓
Data Cleaning
   ↓
Data Validation
   ↓
Database
   ↓
SQL Analytics
   ↓
Python Analytics
   ↓
Root Cause Analysis
   ↓
Machine Learning
   ↓
AI Insights
   ↓
Recommendations
   ↓
Operational Decisions
```

The goal is not simply to build dashboards, but to create a system that moves from:

**Data → Insight → Prediction → Action**

---

# 🚀 Future Improvements

Potential future enhancements include:

* Real-time delivery monitoring
* Live GPS integration
* Real-time traffic APIs
* Demand forecasting
* Rider allocation optimization
* Delivery-zone heatmaps
* Advanced time-series forecasting
* Model performance monitoring
* Explainable ML with SHAP
* Automated alerting
* Cloud deployment
* Role-based dashboards
* Production API using FastAPI

---

# 👩‍💻 Author

**Prisha Shah**

M.Sc. Applied Data Science
SRM Institute of Science and Technology

### Project

**OpsLens AI — Delivery Operations Intelligence Platform**

GitHub:
https://github.com/Prisha-22/OpsLens-AI

---

## ⭐ Project Highlight

> **OpsLens AI combines SQL analytics, Python, PostgreSQL, machine learning, anomaly detection, forecasting, root-cause analysis, and AI-powered recommendations into a unified delivery operations intelligence platform.**
