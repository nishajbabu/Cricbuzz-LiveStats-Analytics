"""
SQL Analytics Page: Interactive Runner for all 25 SQL Business Intelligence Queries.
"""
import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.analytics_service import QUERIES, execute_query

st.set_page_config(page_title="SQL Analytics - Cricbuzz LiveStats", layout="wide")

st.title("🔍 SQL Queries & Analytics (25 Complete Solutions)")
st.write("Execute pre-compiled business intelligence queries across Beginner, Intermediate, and Advanced tiers.")

# Level Filter
col_f1, col_f2 = st.columns([1, 3])
with col_f1:
    level_filter = st.selectbox("Filter by Complexity Level:", ["All Levels", "Beginner", "Intermediate", "Advanced"])

filtered_queries = {}
for q_id, q_data in QUERIES.items():
    if level_filter == "All Levels" or q_data["level"] == level_filter:
        filtered_queries[q_id] = f"{q_data['title']} ({q_data['level']})"

with col_f2:
    selected_query_id = st.selectbox(
        "Select an Analytical Question to Run:",
        options=list(filtered_queries.keys()),
        format_func=lambda x: filtered_queries[x]
    )

if selected_query_id:
    q_info = QUERIES[selected_query_id]
    
    st.subheader(f"📌 {q_info['title']}")
    st.caption(f"Complexity Tier: **{q_info['level']}**")

    # Display SQL query code
    with st.expander("📝 View Underlying SQL Query", expanded=True):
        st.code(q_info["sql"].strip(), language="sql")

    # Execute query
    with st.spinner("Executing query against SQL database..."):
        df_result, sql_code = execute_query(selected_query_id)

    if df_result is not None and not df_result.empty:
        st.write(f"### 📋 Query Output ({len(df_result)} records found)")
        st.dataframe(df_result, use_container_width=True)

        # CSV Download Button
        csv_data = df_result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result as CSV",
            data=csv_data,
            file_name=f"query_{selected_query_id}_results.csv",
            mime="text/csv"
        )

        # Automatic Plotly Visual Chart if numeric data exists
        numeric_cols = df_result.select_dtypes(include=['int64', 'float64']).columns.tolist()
        text_cols = df_result.select_dtypes(include=['object']).columns.tolist()

        if len(text_cols) >= 1 and len(numeric_cols) >= 1:
            with st.expander("📈 Auto-Generated Visual Analytics Chart", expanded=True):
                fig = px.bar(df_result, x=text_cols[0], y=numeric_cols[0],
                             title=f"{numeric_cols[0].replace('_', ' ').title()} by {text_cols[0].replace('_', ' ').title()}",
                             text_auto=True)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Query executed successfully, but returned 0 records.")