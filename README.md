📘 RoadSafe Analytics

🚦 Road Accidents Analysis & Visualization

RoadSafe Analytics is a data analytics project focused on understanding road accident patterns, severity factors, and high-risk locations using the US Accidents dataset.
The project applies data cleaning, exploratory analysis, hypothesis testing, and interactive visualization to support data-driven road safety insights.

🎯 Project Objectives

Analyze road accident data to identify patterns and trends

Understand factors influencing accident severity

Perform time-based, weather-based, and location-based analysis

Visualize accident hotspots and risk zones

Present insights using an interactive dashboard

📊 Dataset

Source: US Accidents Dataset

Key attributes: Severity, Time, Location, Weather, Visibility, Road features

🛠️ Project Workflow
🔹 Milestone 1 – Dataset Acquisition & Understanding

Defined project objectives and outcomes

Explored dataset structure, schema, and statistics

Identified missing values and data types

🔹 Milestone 2 – Data Cleaning & Preprocessing

Handled missing values and duplicates

Converted datetime columns

Engineered features: Hour, Weekday, Month

🔹 Milestone 3 – Exploratory Analysis & Hypothesis Testing

Severity and weather analysis

Time-based accident trends

Geospatial hotspot identification

Hypothesis testing on rush hours and visibility

🔹 Milestone 4 – Visualization & Documentation

Built an interactive Streamlit dashboard

Added maps, charts, and advanced plots

Documented methodology, assumptions, and insights

🖥️ Streamlit Dashboard Features

Interactive filters: Severity, Weekday, City, Hour range

Bar charts, pie charts, box & violin plots

Correlation heatmaps

Static and interactive accident hotspot maps

Final insights and interpretation section

Help tab for usability guidance

📈 Key Insights

Accidents peak during morning and evening rush hours

Majority of accidents occur under good visibility, but severity varies

Bad weather conditions increase accident severity

Accident hotspots are concentrated in urban and highway regions

▶️ How to Run the Dashboard
pip install -r requirements.txt
streamlit run app.py

📂 Repository Structure
├── app.py
├── requirements.txt
├── notebooks/
│   └── week 7_Final_Insights.ipynb
├── RoadSafe_Analytics_Report.docx
└── README.md

✅ Conclusion

This project demonstrates how data analytics and visualization can support road safety planning and decision-making.
The interactive dashboard enables stakeholders to explore accident risks across time, severity, and location dimensions.
