
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="PragyanAI | Job Demand Analytics",
    page_icon="📊",
    layout="wide"
)

REQUIRED_COLUMNS = [
    "reporting_period", "district", "sector", "occupation",
    "indicator", "value", "unit", "source"
]

# --------------------------------------------------
# DEMONSTRATION DATA
# --------------------------------------------------
def create_sample_data():
    records = []

    districts = [
        "Bengaluru Urban", "Mysuru", "Mangaluru",
        "Belagavi", "Kalaburagi", "Hubballi-Dharwad"
    ]

    sectors = {
        "Information Technology": [
            "Data Analyst", "Software Developer",
            "Cloud Engineer", "AI Engineer"
        ],
        "Manufacturing": [
            "Production Engineer", "Quality Analyst",
            "Machine Operator"
        ],
        "Healthcare": [
            "Nurse", "Medical Technician", "Healthcare Assistant"
        ],
        "Retail": [
            "Sales Executive", "Customer Support Executive"
        ],
        "Finance": [
            "Accountant", "Financial Analyst"
        ]
    }

    base_values = {
        "Information Technology": 220,
        "Manufacturing": 170,
        "Healthcare": 140,
        "Retail": 120,
        "Finance": 100
    }

    for period_index, period in enumerate(
        ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
         "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"]
    ):
        for district_index, district in enumerate(districts):
            for sector_index, (sector, occupations) in enumerate(sectors.items()):
                for occupation_index, occupation in enumerate(occupations):
                    value = (
                        base_values[sector]
                        + district_index * 17
                        + occupation_index * 11
                        + period_index * (4 + sector_index)
                    )

                    records.append({
                        "reporting_period": period,
                        "district": district,
                        "sector": sector,
                        "occupation": occupation,
                        "indicator": "Illustrative job postings",
                        "value": value,
                        "unit": "postings",
                        "source": "Synthetic demonstration data"
                    })

    return pd.DataFrame(records)


# --------------------------------------------------
# DATA VALIDATION
# --------------------------------------------------
def prepare_data(data):
    data = data.copy()
    data.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in data.columns
    ]

    # Accept common alternative column names
    aliases = {
        "period": "reporting_period",
        "date": "reporting_period",
        "quarter": "reporting_period",
        "location": "district",
        "city": "district",
        "occupation_name": "occupation",
        "job_role": "occupation",
        "job_title": "occupation",
        "industry": "sector",
        "metric": "indicator",
        "employment_indicator": "indicator",
        "count": "value",
        "vacancies": "value",
        "job_postings": "value",
        "units": "unit",
        "data_source": "source"
    }

    for old_name, new_name in aliases.items():
        if old_name in data.columns and new_name not in data.columns:
            data.rename(columns={old_name: new_name}, inplace=True)

    # Add optional metadata columns if missing
    if "unit" not in data.columns:
        data["unit"] = "records"

    if "source" not in data.columns:
        data["source"] = "Source not provided"

    if "indicator" not in data.columns:
        data["indicator"] = "Unspecified indicator"

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    for column in [
        "reporting_period", "district", "sector",
        "occupation", "indicator", "unit", "source"
    ]:
        data[column] = data[column].astype("string").str.strip()

    data["value"] = pd.to_numeric(data["value"], errors="coerce")

    data = data.dropna(
        subset=[
            "reporting_period", "district", "sector",
            "occupation", "indicator", "value"
        ]
    )

    for column in [
        "reporting_period", "district", "sector",
        "occupation", "indicator", "unit", "source"
    ]:
        data[column] = data[column].fillna("Not specified")
        data.loc[data[column] == "", column] = "Not specified"

    if data.empty:
        raise ValueError("No valid rows remain after data cleaning.")

    return data.reset_index(drop=True)


# --------------------------------------------------
# EXPORT
# --------------------------------------------------
def make_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, index=False, sheet_name="Filtered Analysis")
    return output.getvalue()


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------
st.title("📊 PragyanAI — Job Demand & Sector Analytics")
st.subheader("Module 2 | Project ID: KSISU-02")

st.markdown("""
Explore job-demand indicators across sectors, occupations, districts
and reporting periods. Upload a dataset or start with the included
synthetic demonstration data.
""")

st.info(
    "Data transparency: The default dataset is synthetic demonstration "
    "data. It does not represent measured Karnataka employment, actual "
    "vacancies, or official government statistics."
)

# --------------------------------------------------
# SIDEBAR: DATA INPUT
# --------------------------------------------------
st.sidebar.header("⚙️ Data Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            raw_data = pd.read_csv(uploaded_file)
        else:
            raw_data = pd.read_excel(uploaded_file)

        df = prepare_data(raw_data)
        st.sidebar.success(f"Loaded {len(df):,} valid rows")
    except Exception as error:
        st.error(f"Could not load the uploaded dataset: {error}")
        st.stop()
else:
    df = create_sample_data()
    df = prepare_data(df)
    st.sidebar.caption("Using synthetic demonstration data.")

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

def options_for(column):
    return sorted(df[column].dropna().unique().tolist())

selected_periods = st.sidebar.multiselect(
    "Reporting period",
    options_for("reporting_period"),
    default=options_for("reporting_period")
)

selected_districts = st.sidebar.multiselect(
    "District / location",
    options_for("district"),
    default=options_for("district")
)

selected_sectors = st.sidebar.multiselect(
    "Sector",
    options_for("sector"),
    default=options_for("sector")
)

selected_occupations = st.sidebar.multiselect(
    "Occupation",
    options_for("occupation"),
    default=options_for("occupation")
)

selected_indicators = st.sidebar.multiselect(
    "Demand indicator",
    options_for("indicator"),
    default=options_for("indicator")
)

filtered = df[
    df["reporting_period"].isin(selected_periods)
    & df["district"].isin(selected_districts)
    & df["sector"].isin(selected_sectors)
    & df["occupation"].isin(selected_occupations)
    & df["indicator"].isin(selected_indicators)
].copy()

if filtered.empty:
    st.warning("No data matches your filters. Select at least one value in each filter.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.markdown("### 📌 Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Records analysed", f"{len(filtered):,}")
k2.metric("Sectors", filtered["sector"].nunique())
k3.metric("Occupations", filtered["occupation"].nunique())
k4.metric("Locations", filtered["district"].nunique())

st.caption(
    "Indicator values are aggregated according to the selected filters. "
    "They are not necessarily unique job counts."
)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sector Analysis",
    "🏆 Occupation Ranking",
    "📍 Location Analysis",
    "🕒 Demand Trends",
    "📋 Data & Report"
])

# --------------------------------------------------
# TAB 1: SECTOR ANALYSIS
# --------------------------------------------------
with tab1:
    st.markdown("#### Sector-wise demand indicator")

    sector_data = (
        filtered.groupby(["sector", "unit"], as_index=False)["value"]
        .sum()
        .sort_values("value", ascending=False)
    )

    fig_sector = px.bar(
        sector_data,
        x="sector",
        y="value",
        color="sector",
        hover_data=["unit"],
        title="Aggregated indicator value by sector",
        labels={"value": "Aggregated indicator value", "sector": "Sector"}
    )
    st.plotly_chart(fig_sector, use_container_width=True)

    st.dataframe(sector_data, use_container_width=True, hide_index=True)

# --------------------------------------------------
# TAB 2: OCCUPATION RANKING
# --------------------------------------------------
with tab2:
    st.markdown("#### Leading occupations in the selected data")

    top_n = st.slider("Number of occupations to display", 5, 20, 10)

    occupation_data = (
        filtered.groupby(["occupation", "unit"], as_index=False)["value"]
        .sum()
        .sort_values("value", ascending=False)
        .head(top_n)
    )

    fig_occupation = px.bar(
        occupation_data.sort_values("value"),
        x="value",
        y="occupation",
        color="value",
        orientation="h",
        hover_data=["unit"],
        title=f"Top {top_n} occupations by aggregated indicator value",
        labels={"value": "Aggregated indicator value", "occupation": "Occupation"}
    )
    st.plotly_chart(fig_occupation, use_container_width=True)
    st.dataframe(occupation_data, use_container_width=True, hide_index=True)

# --------------------------------------------------
# TAB 3: LOCATION ANALYSIS
# --------------------------------------------------
with tab3:
    st.markdown("#### Compare district-level indicators")

    district_data = (
        filtered.groupby(["district", "unit"], as_index=False)["value"]
        .sum()
        .sort_values("value", ascending=False)
    )

    fig_district = px.bar(
        district_data,
        x="district",
        y="value",
        color="district",
        hover_data=["unit"],
        title="Aggregated indicator value by district",
        labels={"value": "Aggregated indicator value", "district": "District"}
    )
    st.plotly_chart(fig_district, use_container_width=True)

    st.dataframe(district_data, use_container_width=True, hide_index=True)

    st.caption(
        "Compare districts only when the source, indicator definition, "
        "period and units are comparable. The sample data is illustrative."
    )

# --------------------------------------------------
# TAB 4: TIME SERIES AND GROWTH
# --------------------------------------------------
with tab4:
    st.markdown("#### Indicator trends across reporting periods")

    trend_data = (
        filtered.groupby(
            ["reporting_period", "sector", "unit"], as_index=False
        )["value"].sum()
    )

    fig_trend = px.line(
        trend_data,
        x="reporting_period",
        y="value",
        color="sector",
        markers=True,
        hover_data=["unit"],
        title="Sector-wise indicator trends",
        labels={
            "reporting_period": "Reporting period",
            "value": "Aggregated indicator value",
            "sector": "Sector"
        }
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("#### Period-over-period change")

    # Period ordering is based on the period labels in the data.
    periods = sorted(filtered["reporting_period"].unique())

    if len(periods) >= 2:
        growth_data = (
            filtered.groupby(
                ["reporting_period", "sector", "unit"], as_index=False
            )["value"].sum()
        )

        first_period = periods[-2]
        last_period = periods[-1]

        first = growth_data[
            growth_data["reporting_period"] == first_period
        ].rename(columns={"value": "previous_value"})

        last = growth_data[
            growth_data["reporting_period"] == last_period
        ].rename(columns={"value": "current_value"})

        comparison = last[
            ["sector", "unit", "current_value"]
        ].merge(
            first[["sector", "unit", "previous_value"]],
            on=["sector", "unit"],
            how="inner"
        )

        comparison["change"] = (
            comparison["current_value"] - comparison["previous_value"]
        )

        comparison["growth_percent"] = comparison.apply(
            lambda row: (
                (row["change"] / abs(row["previous_value"])) * 100
                if row["previous_value"] != 0 else float("nan")
            ),
            axis=1
        )

        comparison = comparison.sort_values(
            "growth_percent", ascending=False, na_position="last"
        )

        st.caption(
            f"Comparing {last_period} with {first_period}. "
            "Growth is shown only for matching sectors and units. "
            "A zero previous value has no defined percentage growth."
        )

        st.dataframe(
            comparison.round(2),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "Select at least two reporting periods to calculate period-over-period change."
        )

# --------------------------------------------------
# TAB 5: DATA QUALITY AND DOWNLOAD
# --------------------------------------------------
with tab5:
    st.markdown("#### Data preview")
    st.dataframe(filtered.head(500), use_container_width=True, hide_index=True)

    st.markdown("#### Data quality summary")
    q1, q2, q3 = st.columns(3)
    q1.metric("Rows in source", f"{len(df):,}")
    q2.metric("Rows after filters", f"{len(filtered):,}")
    q3.metric("Missing source labels", int(
        (filtered["source"] == "Source not provided").sum()
    ))

    st.markdown("#### Sources represented")
    sources = filtered["source"].value_counts().rename_axis(
        "source"
    ).reset_index(name="records")
    st.dataframe(sources, use_container_width=True, hide_index=True)

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered data (CSV)",
        data=csv_data,
        file_name="job_demand_analysis.csv",
        mime="text/csv"
    )

    st.download_button(
        "⬇️ Download filtered data (Excel)",
        data=make_excel(filtered),
        file_name="job_demand_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("#### Interpretation")
    st.write(
        "Use the rankings to identify the largest recorded indicator values "
        "in this dataset. Confirm the indicator definition, source, period, "
        "geography and units before making policy conclusions."
    )

st.divider()
st.caption(
    "PragyanAI | KSISU-02 | Job Demand and Sector Analytics | "
    "Evidence-based analysis, with limitations disclosed"
)


