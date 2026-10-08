import streamlit as st  # type: ignore[import-not-found]
import json
from pathlib import Path

# ------------------------------------------------------
# 1. PAGE SETUP & DATA LOADING
# ------------------------------------------------------
st.set_page_config(page_title="Credit Risk Scorecard", page_icon="📊", layout="centered")

# Cache the JSON loading so the app doesn't reload the file on every slider click
@st.cache_data
def load_config():
    config_path = Path("scorecard_config.json")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
scorecard = config["scorecard_points"]

# ------------------------------------------------------
# 2. USER INTERFACE (FRONTEND)
# ------------------------------------------------------
st.title("📊 Credit Risk Scorecard Engine")
st.markdown("Evaluate applicant risk instantly using the deployed logistic regression scorecard rules.")

st.header("Applicant Profile")

# Create input fields based on the features you trained on
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    income = st.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=500.0)
    debt_ratio = st.number_input("Debt Ratio", min_value=0.0, max_value=10.0, value=0.4, step=0.05)

with col2:
    revol_util = st.number_input("Revolving Utilization (%)", min_value=0.0, max_value=2.0, value=0.3, step=0.05)
    open_lines = st.number_input("Open Credit Lines", min_value=0, max_value=50, value=5)
    history_delinq = st.selectbox("Serious Delinquency in Past 2 Yrs?", options=[0, 1])

# ------------------------------------------------------
# 3. SCORING ENGINE (BACKEND LOGIC)
# ------------------------------------------------------
# Helper function to map a continuous input to the correct scorecard bin
def get_points_for_feature(feature_name, user_value, bin_edges, points_dict):
    # This finds the correct bucket for the user's value
    if feature_name not in bin_edges or feature_name not in points_dict:
        return 0

    edges = bin_edges[feature_name]
    intervals = list(points_dict[feature_name].keys())
    if len(edges) < 2 or not intervals:
        return 0
    
    # Simple logic to find the interval the user_value falls into
    for i in range(min(len(edges) - 1, len(intervals))):
        # Include the upper edge only for the final bin to avoid overlap.
        in_bin = edges[i] <= user_value < edges[i + 1]
        if i == len(edges) - 2:
            in_bin = edges[i] <= user_value <= edges[i + 1]
        if in_bin:
            # In a production app, you would match this index to the specific string key in points_dict
            # For this example, we assume we extract the matched points based on the interval
            interval_str = intervals[i]
            return points_dict[feature_name][interval_str]
            
    # Fallback for out-of-bounds extremes
    if user_value < edges[0]:
        return points_dict[feature_name][intervals[0]]
    else:
        return points_dict[feature_name][intervals[-1]]

st.markdown("---")

# Calculate Button
if st.button("Calculate Credit Score", type="primary"):
    
    # Initialize score with the base offset from your calibrator
    final_score = config["calibration"]["offset"]
    
    # 1. Map Age
    if "age" in scorecard:
        final_score += get_points_for_feature("age", age, config["bin_edges"], scorecard)
        
    # 2. Map Income
    if "MonthlyIncome" in scorecard:
        final_score += get_points_for_feature("MonthlyIncome", income, config["bin_edges"], scorecard)
        
    # Map the remaining applicant inputs when those features exist in the config.
    for feature_name, user_value in {
        "DebtRatio": debt_ratio,
        "RevolvingUtilization": revol_util,
        "NumberOfOpenCreditLinesAndLoans": open_lines,
        "NumberOfTimes90DaysLate": history_delinq,
    }.items():
        if feature_name in scorecard:
            final_score += get_points_for_feature(
                feature_name, user_value, config["bin_edges"], scorecard
            )
    
    # Display the final metric
    st.subheader("Final Decision")
    st.metric(label="Calculated Credit Score", value=int(final_score))
    
    if final_score >= 600:
        st.success("Decision: Approved")
    else:
        st.error("Decision: Declined")