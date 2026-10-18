"""
Job Demand and Sector Analytics
Main Streamlit Application - Overview Page
"""
import sys
from pathlib import Path
# Ensure project root is in sys.path for Streamlit Cloud and portability
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import streamlit as st
import pandas as pd
from typing import Dict, Any
from config.settings import APP_TITLE, APP_SUBTITLE, BENCHMARK_DISTRICT
from src.ui_helpers import get_cached_dataset, render_sidebar_header, render_global_filters
from src.indicator_classification import get_indicator_definition
from src.reporting import generate_evidence_summary
st.set_page_config(
    page_title=f"{APP_TITLE} | Overview",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Load data
raw_unified_df, validation_reports = get_cached_dataset()
# Render global filters in sidebar
filtered_df = render_global_filters(raw_unified_df)
# Page Header
st.title(f"📈 {APP_TITLE}")
st.markdown(f"*{APP_SUBTITLE}*")
st.markdown("---")
# Project Introduction & Methodology Guardrails
col_intro, col_provenance = st.columns([3, 2])"""
Job Demand and Sector Analytics
Main Streamlit Application - Overview Page
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any

from config.settings import APP_TITLE, APP_SUBTITLE, BENCHMARK_DISTRICT
from src.ui_helpers import get_cached_dataset, render_sidebar_header, render_global_filters
from src.indicator_classification import get_indicator_definition
from src.reporting import generate_evidence_summary

st.set_page_config(
    page_title=f"{APP_TITLE} | Overview",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
raw_unified_df, validation_reports = get_cached_dataset()

# Render global filters in sidebar
filtered_df = render_global_filters(raw_unified_df)

# Page Header
st.title(f"📈 {APP_TITLE}")
st.markdown(f"*{APP_SUBTITLE}*")
st.markdown("---")

# Project Introduction & Methodology Guardrails
col_intro, col_provenance = st.columns([3, 2])
with col_intro:
    st.subheader("Objective & Empirical Scope")
    st.markdown(
        """
        The **Job Demand and Sector Analytics** platform equips policy analysts, researchers, and workforce 
        planners with evidence-backed insights into labour-market dynamics across Karnataka and national benchmarks.
        
        To ensure strict statistical integrity:
        - **No Generic Aggregation:** Administrative vacancies, survey-based estimates, and digital job-posting proxies 
          are maintained as independent indicators and **never added together**.
        - **Geographic Precision:** District analytics are restricted to authentic district-level returns 
          (e.g., DES registered factories across all 31 Karnataka districts).
        - **Verified Provenance:** All figures trace directly to official gazettes and statistical survey releases.
        """
    )

with col_provenance:
    st.subheader("Data Sources Successfully Loaded")
    for src_name, rep_info in validation_reports.items():
        status_icon = "✅" if rep_info["is_valid"] else "❌"
        st.markdown(f"- {status_icon} **{src_name}**: `{rep_info['valid_records']}` valid observations")

st.markdown("---")

# Metrics Banner - Strict Categorical Separation
st.subheader("📊 Key Indicator Totals (by Indicator Category)")
col1, col2, col3, col4 = st.columns(4)

# Reported Vacancies (Actual vacancy count)
vac_df = filtered_df[filtered_df["indicator_type"] == "Actual vacancy count"]
vac_val = vac_df["value"].sum() if not vac_df.empty else 0
with col1:
    st.metric(
        label="Reported Vacancy Count",
        value=f"{vac_val:,.0f}" if vac_val > 0 else "—",
        help="Explicit statutory/employment exchange notifications (DGE). Not an estimate."
    )

# Estimated Employment (thousands of workers, QES)
est_df = filtered_df[filtered_df["indicator_type"] == "Employment estimate"]
est_val = est_df["value"].mean() if not est_df.empty else 0
with col2:
    st.metric(
        label="Est. Non-Farm Employment",
        value=f"{est_val:,.1f}k" if est_val > 0 else "—",
        help="Estimated mean employment in organized 9 non-farm sectors (Labour Bureau QES)."
    )

# Registered Factory Workforce (DES Karnataka)
fact_df = filtered_df[filtered_df["indicator_name"] == "Registered Factory Employment"]
fact_val = fact_df[fact_df["reporting_period"] == fact_df["reporting_period"].max()]["value"].sum() if not fact_df.empty else 0
with col3:
    st.metric(
        label="Registered Factory Workforce",
        value=f"{fact_val:,.0f}" if fact_val > 0 else "—",
        help="Administrative returns under Factories Act, 1948 across Karnataka districts (DES Karnataka)."
    )

# Observed Online Postings (Job-posting proxy)
post_df = filtered_df[filtered_df["indicator_type"] == "Job-posting count"]
post_val = post_df["value"].sum() if not post_df.empty else 0
with col4:
    st.metric(
        label="Observed Online Job Postings",
        value=f"{post_val:,.0f}" if post_val > 0 else "—",
        help="Digital recruitment demand proxy indexed across tech/digital hubs. Excludes offline openings."
    )

st.markdown("---")

# Dataset Diagnostics & Metadata Details
st.subheader("🔍 Scope & Dimension Coverage")
c_d1, c_d2, c_d3, c_d4, c_d5 = st.columns(5)
c_d1.metric("Valid Observations", f"{len(filtered_df.dropna(subset=['value'])):,}")
c_d2.metric("Sectors Represented", len(filtered_df["sector"].dropna().unique()))
c_d3.metric("Occupations Covered", len(filtered_df["occupation"].dropna().unique()))
c_d4.metric("Districts Represented", len(filtered_df["district"].dropna().unique()))
c_d5.metric("Reporting Periods", len(filtered_df["reporting_period"].dropna().unique()))

# Selected Indicator Definitions
unique_types = filtered_df["indicator_type"].dropna().unique().tolist()
if unique_types:
    st.markdown("### 📖 Indicator Definitions in Active Scope")
    for it in unique_types:
        with st.expander(f"Indicator Type: **{it}**", expanded=False):
            st.info(get_indicator_definition(it))

# Automated Evidence Summary Report Generator
st.markdown("---")
st.subheader("📑 Automated Evidence-Backed Summary Report")
st.markdown(
    "Generate and download an evidence-based synthesis compiled strictly from the loaded records."
)

report_md = generate_evidence_summary(filtered_df)

col_rep_btn, col_rep_view = st.columns([1, 4])
with col_rep_btn:
    st.download_button(
        label="📥 Download Summary Report (.md)",
        data=report_md,
        file_name="job_demand_sector_analytics_summary.md",
        mime="text/markdown",
        use_container_width=True
    )

with st.expander("👁️ Preview Generated Evidence Summary", expanded=False):
    st.markdown(report_md)
