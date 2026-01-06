import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
st.markdown("""
Comprehensive dashboard covering **Week 3 (EDA)** and **Week 4 (Severity Analysis)**
of the Road Safe Analytics project.
""")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/US_Accidents_Cleaned.csv", nrows=200000)
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

severity_filter = st.sidebar.multiselect(
    "Severity Level",
    sorted(df["Severity"].unique()),
    default=sorted(df["Severity"].unique())
)

weekday_filter = st.sidebar.multiselect(
    "Weekday",
    df["Weekday"].unique(),
    default=df["Weekday"].unique()
)

filtered_df = df[
    (df["Severity"].isin(severity_filter)) &
    (df["Weekday"].isin(weekday_filter))
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
st.subheader("📌 Key Statistics")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Accidents", len(filtered_df))
c2.metric("Severity Levels", filtered_df["Severity"].nunique())
c3.metric("Weather Types", filtered_df["Weather_Condition"].nunique())
c4.metric("Road Types", filtered_df["Street"].nunique())

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Exploratory Analysis",
    "⏱ Time and Road Analysis",
    "⚠ Severity Insights",
    "🌍 Geo and Insights"
])


# ==================================================
# TAB 1: WEEK 3 – EDA
# ==================================================
with tab1:
    st.subheader("Accident Severity Distribution")

    fig, ax = plt.subplots()
    filtered_df["Severity"].value_counts().sort_index().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Severity Histogram")

    fig, ax = plt.subplots()
    filtered_df["Severity"].plot(kind="hist", bins=4, ax=ax)
    st.pyplot(fig)

    st.subheader("Top 10 Weather Conditions")

    fig, ax = plt.subplots(figsize=(10,4))
    filtered_df["Weather_Condition"].value_counts().head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)

# ==================================================
# TAB 2: TIME & ROAD ANALYSIS
# ==================================================
with tab2:
    st.subheader("Accidents by Hour")

    fig, ax = plt.subplots(figsize=(10,4))
    filtered_df["Hour"].value_counts().sort_index().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Accidents by Weekday")

    fig, ax = plt.subplots(figsize=(10,4))
    filtered_df["Weekday"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Accidents by Month")

    fig, ax = plt.subplots(figsize=(10,4))
    filtered_df["Month"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Top Road Types (Street)")

    fig, ax = plt.subplots(figsize=(10,4))
    filtered_df["Street"].value_counts().head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Top 5 Road Types – Share")

    fig, ax = plt.subplots(figsize=(6,6))
    filtered_df["Street"].value_counts().head(5).plot(
        kind="pie", autopct="%1.1f%%", ax=ax
    )
    ax.set_ylabel("")
    st.pyplot(fig)

# ==================================================
# TAB 3: WEEK 4 – SEVERITY ANALYSIS
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

    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(x="Severity", y="Visibility(mi)", data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Severity vs Temperature")

    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(x="Severity", y="Temperature(F)", data=filtered_df, ax=ax)
    st.pyplot(fig)

    st.subheader("Weather Condition vs Severity")

    fig, ax = plt.subplots(figsize=(10,4))
    pd.crosstab(
        filtered_df["Weather_Condition"],
        filtered_df["Severity"]
    ).head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Severity vs Junction")

    fig, ax = plt.subplots(figsize=(6,4))
    pd.crosstab(
        filtered_df["Junction"],
        filtered_df["Severity"]
    ).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Severity vs Traffic Signal")

    fig, ax = plt.subplots(figsize=(6,4))
    pd.crosstab(
        filtered_df["Traffic_Signal"],
        filtered_df["Severity"]
    ).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.subheader("Pair Plot (Sampled)")

    sample_df = corr_df.sample(3000)
    pair_fig = sns.pairplot(sample_df, hue="Severity", diag_kind="kde")
    st.pyplot(pair_fig)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown("📘 **Road Safe Analytics Dashboard – Complete Week 3 & 4 Analysis**")

# ==================================================
# TAB 4: MILESTONE 3 – GEOSPATIAL & INSIGHT ANALYSIS
# ==================================================
with tab4:
    st.subheader("🌍 Accident Hotspot Analysis (Week 5)")

    st.markdown("""
    This visualization combines **density-based aggregation** and **scatter plotting**
    to clearly identify accident hotspots across geographic locations.
    """)

    # Sample data for performance
    geo_df = filtered_df.sample(
        min(20000, len(filtered_df)),
        random_state=42
    )

    fig, ax = plt.subplots(figsize=(9,6))

    # Density layer
    sns.histplot(
        x=geo_df["Start_Lng"],
        y=geo_df["Start_Lat"],
        bins=200,
        cmap="Reds",
        ax=ax
    )

    # Scatter layer
    ax.scatter(
        geo_df["Start_Lng"],
        geo_df["Start_Lat"],
        s=1,
        alpha=0.05,
        color="black"
    )

    ax.set_title("Accident Hotspots Across the US (Density + Scatter)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    st.pyplot(fig)

    # -------------------------------
    # Top States & Cities
    # -------------------------------
    st.subheader("📍 Top Accident-Prone Locations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top 5 States**")
        top_states = filtered_df["State"].value_counts().head(5)

        fig, ax = plt.subplots()
        top_states.plot(kind="bar", ax=ax)
        ax.set_ylabel("Accident Count")
        st.pyplot(fig)

    with col2:
        st.markdown("**Top 5 Cities**")
        top_cities = filtered_df["City"].value_counts().head(5)

        fig, ax = plt.subplots()
        top_cities.plot(kind="bar", ax=ax)
        ax.set_ylabel("Accident Count")
        st.pyplot(fig)

    # ==================================================
    # WEEK 6 – INSIGHT EXTRACTION & HYPOTHESIS TESTING
    # ==================================================
    st.subheader("🧠 Insight Extraction & Hypothesis Testing (Week 6)")

    # Q1: Peak accident hour
    st.markdown("### ⏰ What time of day has the most accidents?")

    hour_counts = filtered_df["Hour"].value_counts().sort_index()

    fig, ax = plt.subplots()
    hour_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Accident Count")
    st.pyplot(fig)

    peak_hour = hour_counts.idxmax()
    st.success(f"🔍 **Insight:** Most accidents occur around **{peak_hour}:00 hours**.")

    # Q2: Severity during Rain vs Fog
    st.markdown("### 🌧️ Are accidents more severe during rain or fog?")

    weather_df = filtered_df[
        filtered_df["Weather_Condition"].isin(["Rain", "Fog"])
    ]

    if not weather_df.empty:
        fig, ax = plt.subplots()
        sns.boxplot(
            x="Weather_Condition",
            y="Severity",
            data=weather_df,
            ax=ax
        )
        st.pyplot(fig)

        st.info(
            "📌 **Observation:** Rain-related accidents tend to show "
            "higher severity due to reduced visibility."
        )
    else:
        st.warning("Rain/Fog data not sufficient for comparison.")

    # Q3: Visibility vs Severity
    st.markdown("### 👁️ Is there a correlation between visibility and severity?")

    corr_val = filtered_df["Severity"].corr(
        filtered_df["Visibility(mi)"]
    )

    fig, ax = plt.subplots()
    sns.scatterplot(
        x="Visibility(mi)",
        y="Severity",
        data=filtered_df,
        alpha=0.3,
        ax=ax
    )
    st.pyplot(fig)

    st.success(
        f"📉 **Correlation:** Severity and visibility show a "
        f"{'negative' if corr_val < 0 else 'positive'} correlation "
        f"(r = {corr_val:.2f})."
    )

    # Final Summary
    st.markdown("### ✅ Milestone 3 Summary")
    st.markdown("""
    - Accident hotspots are concentrated in urban and high-traffic regions  
    - Peak accidents occur during rush hours  
    - Rain conditions increase accident severity  
    - Reduced visibility correlates with higher severity  

    These insights support data-driven road safety planning and risk mitigation.
    """)

