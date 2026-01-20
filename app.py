import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Road Safe Analytics Dashboard",
    page_icon="🚦",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🚦 Road Safe Analytics Dashboard")
st.markdown("**Comprehensive dashboard covering all milestones**")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/US_Accidents_Cleaned.csv", nrows=1000000)

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(df["Severity"].unique()),
    default=sorted(df["Severity"].unique())
)

weekday_filter = st.sidebar.multiselect(
    "Weekday",
    df["Weekday"].unique(),
    default=df["Weekday"].unique()
)

city_filter = st.sidebar.multiselect(
    "City",
    sorted(df["City"].dropna().unique())
)

filtered_df = df[
    (df["Severity"].isin(severity_filter)) &
    (df["Weekday"].isin(weekday_filter))
]

if city_filter:
    filtered_df = filtered_df[filtered_df["City"].isin(city_filter)]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
st.subheader("📌 Key Statistics")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Accidents", len(filtered_df))
c2.metric("Average Severity", round(filtered_df["Severity"].mean(), 2))
c3.metric("Weather Types", filtered_df["Weather_Condition"].nunique())
c4.metric("Cities Selected", filtered_df["City"].nunique())

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 EDA",
    "⏱ Time Analysis",
    "⚠ Severity Analysis",
    "🌍 Geo & Hypothesis",
    "📖 Visualizaon and Interpretation",
    "🗺 Interactive Risk Map"
])

# ==================================================
# TAB 1 – EDA (Week 3)
# ==================================================
with tab1:
    st.subheader("Accident Severity Distribution")
    fig, ax = plt.subplots()
    filtered_df["Severity"].value_counts().sort_index().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Top Weather Conditions")
    fig, ax = plt.subplots(figsize=(10,4))
    filtered_df["Weather_Condition"].value_counts().head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)

# ==================================================
# TAB 2 – TIME ANALYSIS
# ==================================================
with tab2:
    st.subheader("Accidents by Hour")
    fig, ax = plt.subplots()
    filtered_df["Hour"].value_counts().sort_index().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Accidents by Month")
    fig, ax = plt.subplots()
    filtered_df["Month"].value_counts().sort_index().plot(kind="line", marker="o", ax=ax)
    st.pyplot(fig)

# ==================================================
# TAB 3 – SEVERITY ANALYSIS (Week 4)
# ==================================================
with tab3:
    st.subheader("Correlation Heatmap")

    corr_cols = [
        "Severity",
        "Visibility(mi)",
        "Temperature(F)",
        "Humidity(%)",
        "Pressure(in)",
        "Wind_Speed(mph)"
    ]
    corr_df = filtered_df[corr_cols].dropna()

    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.subheader("Severity vs Visibility")

    vis_df = filtered_df[filtered_df["Visibility(mi)"] < 10]

    if len(vis_df) < 50:
        st.warning("Low-visibility data is limited. Showing full visibility range.")
        vis_df = filtered_df

    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(x="Severity", y="Visibility(mi)", data=vis_df, ax=ax)
    ax.set_title("Severity vs Visibility")
    st.pyplot(fig)

# ==================================================
# TAB 4 – GEO & HYPOTHESIS (Week 5 & 6)
# ==================================================
with tab4:
    st.subheader("Accident Hotspots (Static Density View)")

    geo_df = filtered_df.sample(min(20000, len(filtered_df)), random_state=42)

    fig, ax = plt.subplots(figsize=(8,6))
    sns.histplot(
        x=geo_df["Start_Lng"],
        y=geo_df["Start_Lat"],
        bins=200,
        cmap="Reds",
        ax=ax
    )
    st.pyplot(fig)

    st.subheader("Hypothesis Testing")

    peak_hour = filtered_df["Hour"].value_counts().idxmax()
    st.success(f"Peak accident hour: {peak_hour}:00")

    corr_val = filtered_df["Severity"].corr(filtered_df["Visibility(mi)"])
    st.info(f"Visibility vs Severity Correlation: {corr_val:.2f}")

# ==================================================
# TAB 5 – FINAL INSIGHTS (Week 7)
# ==================================================
with tab5:
    st.header("📖Visualizaon and Interpretation")

    fig, ax = plt.subplots()
    filtered_df["Hour"].value_counts().sort_index().plot(kind="line", marker="o", ax=ax)
    st.pyplot(fig)
    st.success("Accidents peak during morning and evening rush hours.")

    weather_sev = (
        filtered_df.groupby("Weather_Condition")["Severity"]
        .mean()
        .sort_values(ascending=False)
        .head(8)
    )
    fig, ax = plt.subplots()
    weather_sev.plot(kind="bar", ax=ax)
    st.pyplot(fig)
    st.success("Rain and fog conditions increase accident severity.")

    st.info("Urban areas and highways require focused safety interventions.")

# ==================================================
# TAB 6 – INTERACTIVE RISK MAP (BONUS FEATURE)
# ==================================================
with tab6:
    st.subheader("🗺 Interactive Accident Danger Hotspots")

    map_df = filtered_df[
        ["Start_Lat", "Start_Lng", "Severity"]
    ].dropna()

    map_df = map_df.sample(min(8000, len(map_df)), random_state=42)

    center_lat = map_df["Start_Lat"].mean()
    center_lng = map_df["Start_Lng"].mean()

    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=4,
        tiles="OpenStreetMap"
    )

    heat_data = [
        [row["Start_Lat"], row["Start_Lng"], row["Severity"]]
        for _, row in map_df.iterrows()
    ]

    HeatMap(
        heat_data,
        radius=8,
        blur=10,
        max_zoom=6
    ).add_to(m)

    st_folium(m, width=1000, height=500)

    st.success("Darker regions indicate higher accident risk.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown("🚦 RoadSafe Analytics | Milestone 4 – Final Dashboard")
