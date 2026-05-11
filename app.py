import streamlit as st
import pandas as pd

from src.data_loader import load_835
from src.data_loader import load_837

from src.preprocess import merge_claims

from src.denial_engine import analyze_claim

from src.similarity_engine import build_similarity

from src.clustering import cluster_claims

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Claim Denial Analyzer",
    page_icon="🏥",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .title {
        font-size: 48px;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 18px;
        color: #A0A0A0;
        margin-bottom: 30px;
    }

    .metric-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #30363D;
    }

    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #58A6FF;
    }

    .metric-label {
        font-size: 16px;
        color: #C9D1D9;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("🏥 Navigation")

st.sidebar.markdown("---")

st.sidebar.info(
    "AI-Powered Healthcare Claim Denial Analysis System"
)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.markdown(
    '<div class="title">AI Claim Denial Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Healthcare RCM Denial Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

try:

    df835 = load_835("data/835_claims.csv")

    df837 = load_837("data/837_claims.csv")

    merged_df = merge_claims(df835, df837)

    st.success("✅ Data Loaded Successfully")

except Exception as e:

    st.error(f"Error Loading Data: {e}")

    st.stop()

# ------------------------------------------------
# ANALYSIS
# ------------------------------------------------

results = []

for index, row in merged_df.iterrows():

    analysis = analyze_claim(row)

    results.append(analysis)

results_df = pd.DataFrame(results)

# ------------------------------------------------
# KPI METRICS
# ------------------------------------------------

st.markdown("## 📊 Dashboard Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-value">{len(merged_df)}</div>
            <div class="metric-label">Total Claims</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col2:

    denied_count = len(
        merged_df[
            merged_df["pc_ClaimStatus"] == 4
        ]
    )

    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-value">{denied_count}</div>
            <div class="metric-label">Denied Claims</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col3:

    total_amount = merged_df[
        "pc_ClaimAmount"
    ].sum()

    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-value">${total_amount:,.0f}</div>
            <div class="metric-label">Total Claim Amount</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col4:

    avg_confidence = round(
        results_df["confidence"].mean(),
        2
    )

    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-value">{avg_confidence}</div>
            <div class="metric-label">Avg Confidence</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

st.markdown("---")

# ------------------------------------------------
# MERGED CLAIMS DATA
# ------------------------------------------------

st.subheader("📁 Merged Claims Data")

st.dataframe(
    merged_df.head(10),
    use_container_width=True
)

# ------------------------------------------------
# DENIAL ANALYSIS
# ------------------------------------------------

st.subheader("🧠 Denial Analysis")

st.markdown("### Sample JSON Output")

st.json(results[0])

st.markdown("### Full Analysis Table")

st.dataframe(
    results_df,
    use_container_width=True
)

# ------------------------------------------------
# HISTORICAL SIMILARITY
# ------------------------------------------------

st.subheader("🔍 Historical Similarity Analysis")

similarity_matrix = build_similarity(merged_df)

similarity_df = pd.DataFrame(similarity_matrix)

st.dataframe(
    similarity_df.head(10),
    use_container_width=True
)

# ------------------------------------------------
# CLUSTERING
# ------------------------------------------------

st.subheader("🧩 Claim Clustering")

clustered_df = cluster_claims(merged_df)

st.dataframe(
    clustered_df[
        [
            "pc_ClaimID",
            "pc_ClaimAmount",
            "cluster"
        ]
    ],
    use_container_width=True
)

# ------------------------------------------------
# CLUSTER SUMMARY
# ------------------------------------------------

st.subheader("📌 Cluster Summary")

cluster_summary = clustered_df.groupby(
    "cluster"
).agg({

    "pc_ClaimAmount": "sum",

    "pc_ClaimID": "count"

}).reset_index()

cluster_summary.columns = [

    "Cluster",

    "Total Amount",

    "Claim Count"
]

st.dataframe(
    cluster_summary,
    use_container_width=True
)

# ------------------------------------------------
# DOWNLOAD BUTTON
# ------------------------------------------------

st.subheader("⬇️ Download Results")

csv = results_df.to_csv(index=False)

st.download_button(
    label="Download Analysis CSV",
    data=csv,
    file_name="claim_analysis.csv",
    mime="text/csv"
)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.caption(
    "Built for Gabeo AI ML Engineer Assignment"
)


