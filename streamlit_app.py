
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Global Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- GITHUB DATASET ----------------
GITHUB_URL = "https://raw.githubusercontent.com/USERNAME/REPOSITORY/main/dataset.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(GITHUB_URL)

    # Data cleaning
    df = df.drop_duplicates()
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load GitHub dataset: {e}")
    st.stop()

# ---------------- TITLE ----------------
st.title("📊 Global Sales Analysis Dashboard")
st.caption("Dataset automatically loaded from GitHub")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎛️ Dashboard Filters")

# Automatically identify categorical columns
categorical_cols = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

# Automatically identify numeric columns
numeric_cols = df.select_dtypes(
    include=["number"]
).columns.tolist()

filtered_df = df.copy()

# Sidebar filters
for col in categorical_cols:
    values = sorted(df[col].dropna().unique().tolist(), key=str)

    selected = st.sidebar.multiselect(
        f"Select {col}",
        values,
        default=values
    )

    filtered_df = filtered_df[
        filtered_df[col].isin(selected)
    ]

# ---------------- KPI CARDS ----------------
st.subheader("📌 Key Performance Indicators")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Records", len(filtered_df))

with c2:
    st.metric("Numeric Columns", len(numeric_cols))

with c3:
    st.metric("Total Columns", len(df.columns))

st.divider()

# ---------------- DATA PREVIEW ----------------
with st.expander("View Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# ---------------- CHART SELECTION ----------------
if len(filtered_df) == 0:
    st.warning("No records available for the selected filters.")
    st.stop()

if not numeric_cols:
    st.warning("Dataset has no numeric columns for plotting.")
    st.stop()

x_col = st.selectbox("Select X-axis", df.columns)
y_col = st.selectbox(
    "Select Y-axis",
    numeric_cols,
    index=0
)

# ---------------- BAR CHART ----------------
st.subheader("📊 Bar Chart")

fig1 = px.bar(
    filtered_df,
    x=x_col,
    y=y_col,
    title=f"{y_col} by {x_col}",
    color=x_col
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- LINE CHART ----------------
st.subheader("📈 Line Chart")

fig2 = px.line(
    filtered_df,
    x=x_col,
    y=y_col,
    title=f"{y_col} Trend"
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------- PIE CHART ----------------
st.subheader("🥧 Pie Chart")

pie_col = st.selectbox(
    "Select Pie Chart Category",
    categorical_cols if categorical_cols else df.columns
)

pie_data = filtered_df[pie_col].value_counts().reset_index()
pie_data.columns = [pie_col, "Count"]

fig3 = px.pie(
    pie_data,
    names=pie_col,
    values="Count",
    title=f"Distribution of {pie_col}"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- HISTOGRAM ----------------
st.subheader("📉 Histogram")

hist_col = st.selectbox(
    "Select Histogram Column",
    numeric_cols
)

fig4 = px.histogram(
    filtered_df,
    x=hist_col,
    title=f"Distribution of {hist_col}"
)
st.plotly_chart(fig4, use_container_width=True)

# ---------------- SCATTER PLOT ----------------
st.subheader("🔵 Scatter Plot")

scatter_y = st.selectbox(
    "Select Scatter Y-axis",
    numeric_cols
)

fig5 = px.scatter(
    filtered_df,
    x=y_col,
    y=scatter_y,
    title="Relationship Between Variables"
)
st.plotly_chart(fig5, use_container_width=True)

# ---------------- FOOTER ----------------
st.success("Dashboard loaded successfully from GitHub!")
