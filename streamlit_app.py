
import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= GITHUB DATASET =================
GITHUB_URL = "https://raw.githubusercontent.com/kuruvamanasa016-hub/Supermarketsales/main/supermarket_sales%20-.csv"


# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv(GITHUB_URL)

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()

    # Convert numeric columns
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors="coerce")

        if converted.notna().sum() > 0:
            df[col] = converted

    # Convert date column if available
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"], dayfirst=True, errors="coerce"
        )

    return df


try:
    df = load_data()

except Exception as e:
    st.error("Unable to load dataset from GitHub.")
    st.error(str(e))
    st.stop()


# ================= DASHBOARD TITLE =================
st.title("📊 Supermarket Sales Analysis Dashboard")
st.caption("Interactive Sales Analytics | Dataset loaded automatically from GitHub")

st.divider()


# ================= SIDEBAR FILTERS =================
st.sidebar.title("🎛️ Dashboard Filters")

# Exclude high-cardinality identifier and time columns
categorical_cols = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

dimension_cols = [
    col for col in categorical_cols
    if col.lower() not in ["invoice id", "date", "time"]
]

filtered_df = df.copy()

for col in dimension_cols:

    values = sorted(
        df[col].dropna().unique().tolist(),
        key=str
    )

    selected = st.sidebar.multiselect(
        f"Filter {col}",
        options=values,
        default=values
    )

    filtered_df = filtered_df[
        filtered_df[col].isin(selected)
    ]


if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()


# ================= KPI CARDS =================
st.subheader("📌 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Transactions", len(filtered_df))

with c2:
    if "Total" in filtered_df.columns:
        st.metric(
            "Total Sales",
            f"${filtered_df['Total'].sum():,.2f}"
        )
    else:
        st.metric("Total Sales", "N/A")

with c3:
    if "gross income" in filtered_df.columns:
        st.metric(
            "Gross Income",
            f"${filtered_df['gross income'].sum():,.2f}"
        )
    else:
        st.metric("Gross Income", "N/A")

with c4:
    if "Rating" in filtered_df.columns:
        st.metric(
            "Average Rating",
            f"{filtered_df['Rating'].mean():.2f} / 10"
        )
    else:
        st.metric("Numeric Columns", len(
            filtered_df.select_dtypes(include="number").columns
        ))

st.divider()


# ================= DATA PREVIEW =================
with st.expander("📁 View Dataset"):
    st.dataframe(filtered_df, use_container_width=True)


# ================= CHART SETTINGS =================
numeric_cols = filtered_df.select_dtypes(
    include="number"
).columns.tolist()

if not numeric_cols:
    st.warning("No numeric columns available.")
    st.stop()

if not dimension_cols:
    st.warning("No categorical columns available for grouping.")
    st.stop()

st.subheader("📊 Sales Analysis and Visualization")

metric_default = (
    numeric_cols.index("Total")
    if "Total" in numeric_cols else 0
)

y_col = st.selectbox(
    "Select Sales Metric",
    numeric_cols,
    index=metric_default
)

x_col = st.selectbox(
    "Select Category",
    dimension_cols,
    index=dimension_cols.index("Product line")
    if "Product line" in dimension_cols else 0
)

aggregation = st.selectbox(
    "Select Aggregation",
    ["Sum", "Average", "Count"]
)

agg_function = {
    "Sum": "sum",
    "Average": "mean",
    "Count": "count"
}[aggregation]

# Aggregate records to avoid overcrowded graphs
grouped_data = (
    filtered_df.groupby(x_col, observed=True)[y_col]
    .agg(agg_function)
    .reset_index()
    .sort_values(y_col, ascending=False)
)

# ================= BAR CHART =================
st.subheader("📊 1. Category-wise Bar Chart")

top_n = st.slider(
    "Number of categories to display",
    min_value=3,
    max_value=min(10, len(grouped_data)),
    value=min(7, len(grouped_data))
)

bar_data = grouped_data.head(top_n)

fig1 = px.bar(
    bar_data,
    x=x_col,
    y=y_col,
    color=x_col,
    text_auto=".2s",
    title=f"{aggregation} {y_col} by {x_col}"
)

fig1.update_layout(
    height=480,
    showlegend=False,
    xaxis_title=x_col,
    yaxis_title=y_col,
    bargap=0.35,
    template="plotly_white"
)

fig1.update_traces(
    textposition="outside",
    cliponaxis=False
)

st.plotly_chart(
    fig1,
    use_container_width=True,
    config={"displayModeBar": True}
)


# ================= LINE CHART =================
st.subheader("📈 2. Sales Trend Analysis")

if "Date" in filtered_df.columns:

    trend_data = (
        filtered_df.dropna(subset=["Date"])
        .groupby("Date")[y_col]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    fig2 = px.line(
        trend_data,
        x="Date",
        y=y_col,
        markers=True,
        title=f"Daily {y_col} Trend"
    )

else:

    fig2 = px.line(
        grouped_data.sort_values(x_col),
        x=x_col,
        y=y_col,
        markers=True,
        title=f"{y_col} Trend by {x_col}"
    )

fig2.update_layout(
    height=450,
    template="plotly_white",
    xaxis_title="Date / Category",
    yaxis_title=y_col
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ================= PIE CHART =================
st.subheader("🥧 3. Sales Distribution")

pie_data = grouped_data.copy()

fig3 = px.pie(
    pie_data,
    names=x_col,
    values=y_col,
    hole=0.35,
    title=f"{y_col} Distribution by {x_col}"
)

fig3.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig3.update_layout(
    height=500,
    template="plotly_white"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ================= HISTOGRAM =================
st.subheader("📉 4. Data Distribution Histogram")

hist_col = st.selectbox(
    "Select Histogram Metric",
    numeric_cols,
    index=metric_default,
    key="histogram"
)

fig4 = px.histogram(
    filtered_df,
    x=hist_col,
    nbins=20,
    title=f"Distribution of {hist_col}"
)

fig4.update_layout(
    height=450,
    bargap=0.12,
    template="plotly_white",
    xaxis_title=hist_col,
    yaxis_title="Frequency"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# ================= SCATTER PLOT =================
st.subheader("🔵 5. Relationship Between Variables")

scatter_x = st.selectbox(
    "Select X-axis",
    numeric_cols,
    index=metric_default,
    key="scatter_x"
)

scatter_y = st.selectbox(
    "Select Y-axis",
    numeric_cols,
    index=min(1, len(numeric_cols) - 1),
    key="scatter_y"
)

# Limit points to maintain chart readability
scatter_data = filtered_df[[scatter_x, scatter_y]].dropna()

if len(scatter_data) > 500:
    scatter_data = scatter_data.sample(
        n=500,
        random_state=42
    )

fig5 = px.scatter(
    scatter_data,
    x=scatter_x,
    y=scatter_y,
    opacity=0.55,
    title=f"{scatter_y} vs {scatter_x}"
)

fig5.update_traces(
    marker=dict(size=7)
)

fig5.update_layout(
    height=480,
    template="plotly_white"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# ================= FOOTER =================
st.divider()

st.success(
    "Dashboard successfully loaded from GitHub!"
)

st.caption(
    "Supermarket Sales Analytics | Interactive Data Visualization"
)
