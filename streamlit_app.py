
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Global Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------- PAGE DESIGN ----------
st.title("🛒 Global Supermarket Sales Analysis")
st.caption(
    "Interactive Data Visualization Dashboard | "
    "Explore sales, products, customers, and cities"
)

# ---------- COLUMN DETECTION ----------
def find_column(df, candidates):
    """Find a column using common alternative names."""
    normalized = {
        str(col).strip().lower().replace("_", " ").replace("-", " "): col
        for col in df.columns
    }

    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]

    for col in df.columns:
        name = str(col).strip().lower().replace("_", " ").replace("-", " ")
        if any(candidate in name for candidate in candidates):
            return col

    return None


# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader(
    "Upload your supermarket CSV dataset",
    type=["csv"],
    help="Upload a CSV file containing supermarket sales records."
)

if uploaded_file is None:
    st.info("👆 Upload your CSV file to begin the analysis.")
    st.write("Your dashboard will display KPIs, filters, charts, and data summaries.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file)
except Exception as error:
    st.error(f"Could not read this CSV file: {error}")
    st.stop()

if df.empty or len(df.columns) == 0:
    st.error("The uploaded CSV file is empty.")
    st.stop()

# Remove completely empty rows and columns
df = df.dropna(how="all").dropna(axis=1, how="all").copy()

if df.empty:
    st.error("No usable records were found in the uploaded file.")
    st.stop()

# ---------- DETECT IMPORTANT COLUMNS ----------
city_col = find_column(df, ["city", "branch", "location", "region"])
category_col = find_column(
    df, ["product line", "product category", "category", "product"]
)
customer_col = find_column(
    df, ["customer type", "customer segment", "customer"]
)
payment_col = find_column(df, ["payment", "payment method"])
date_col = find_column(df, ["date", "order date", "invoice date"])
quantity_col = find_column(df, ["quantity", "units sold", "items sold"])
sales_col = find_column(
    df, ["total sales", "total", "revenue", "sales amount", "sales", "amount"]
)

# Prepare numerical columns
if sales_col:
    df[sales_col] = pd.to_numeric(
        df[sales_col].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

if quantity_col:
    df[quantity_col] = pd.to_numeric(df[quantity_col], errors="coerce")

# Parse dates when available
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=False)

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔎 Dashboard Filters")

filtered_df = df.copy()

def apply_category_filter(data, column, label):
    if column is None:
        return data

    options = sorted(data[column].dropna().astype(str).unique().tolist())

    if not options:
        return data

    selected = st.sidebar.multiselect(
        label,
        options,
        default=options,
        key=f"filter_{column}"
    )

    return data[data[column].astype(str).isin(selected)]

filtered_df = apply_category_filter(filtered_df, city_col, "Select City")
filtered_df = apply_category_filter(filtered_df, category_col, "Product Category")
filtered_df = apply_category_filter(filtered_df, customer_col, "Customer Type")
filtered_df = apply_category_filter(filtered_df, payment_col, "Payment Method")

if date_col and filtered_df[date_col].notna().any():
    valid_dates = filtered_df[date_col].dropna()
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="sales_date_filter"
    )

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_df = filtered_df[
            filtered_df[date_col].dt.date.between(start_date, end_date)
        ]

if filtered_df.empty:
    st.warning("No records match the selected filters. Change your filters.")
    st.stop()

# ---------- KPI CARDS ----------
st.subheader("📊 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Records", f"{len(filtered_df):,}")

if sales_col:
    total_sales = filtered_df[sales_col].sum()
    average_sales = filtered_df[sales_col].mean()
    k2.metric("Total Sales", f"{total_sales:,.2f}")
    k3.metric(
        "Average Sales",
        f"{average_sales:,.2f}" if pd.notna(average_sales) else "N/A"
    )
else:
    k2.metric("Total Sales", "Not detected")
    k3.metric("Average Sales", "Not detected")

if quantity_col:
    k4.metric(
        "Total Quantity",
        f"{filtered_df[quantity_col].sum():,.0f}"
    )
else:
    k4.metric("Total Quantity", "Not detected")

st.divider()

# ---------- CHARTS ----------
if sales_col:
    st.subheader("📍 Sales Analysis")

    left, right = st.columns(2)

    # Sales by city
    if city_col:
        city_sales = (
            filtered_df.groupby(city_col, dropna=False)[sales_col]
            .sum()
            .reset_index()
            .sort_values(sales_col, ascending=False)
        )

        with left:
            fig_city = px.bar(
                city_sales,
                x=city_col,
                y=sales_col,
                color=city_col,
                title="Total Sales by City",
                labels={sales_col: "Total Sales", city_col: "City"},
                text_auto=".2s"
            )
            st.plotly_chart(
                fig_city, use_container_width=True, key="sales_by_city"
            )

    # Sales by product category
    if category_col:
        category_sales = (
            filtered_df.groupby(category_col, dropna=False)[sales_col]
            .sum()
            .reset_index()
            .sort_values(sales_col, ascending=False)
        )

        with right:
            fig_category = px.bar(
                category_sales,
                x=category_col,
                y=sales_col,
                color=category_col,
                title="Sales by Product Category",
                labels={sales_col: "Total Sales"},
                text_auto=".2s"
            )
            st.plotly_chart(
                fig_category,
                use_container_width=True,
                key="sales_by_category"
            )

    # Pie chart
    if category_col:
        st.subheader("🍰 Sales Share by Product Category")

        category_share = (
            filtered_df.groupby(category_col, dropna=False)[sales_col]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            category_share,
            names=category_col,
            values=sales_col,
            hole=0.4,
            title="Percentage of Total Sales by Category"
        )
        st.plotly_chart(
            fig_pie, use_container_width=True, key="sales_category_pie"
        )

    # Sales trend
    if date_col and filtered_df[date_col].notna().any():
        st.subheader("📈 Sales Trend Over Time")

        trend_data = filtered_df.dropna(subset=[date_col]).copy()
        trend_data["Period"] = trend_data[date_col].dt.to_period("M").astype(str)

        trend = (
            trend_data.groupby("Period", as_index=False)[sales_col]
            .sum()
            .sort_values("Period")
        )

        fig_trend = px.line(
            trend,
            x="Period",
            y=sales_col,
            markers=True,
            title="Monthly Sales Trend",
            labels={"Period": "Month", sales_col: "Total Sales"}
        )
        st.plotly_chart(
            fig_trend, use_container_width=True, key="monthly_sales_trend"
        )

    # Distribution of transaction sales
    st.subheader("📉 Sales Distribution")

    fig_hist = px.histogram(
        filtered_df.dropna(subset=[sales_col]),
        x=sales_col,
        nbins=20,
        title="Distribution of Transaction Amounts",
        labels={sales_col: "Sales Amount"}
    )
    st.plotly_chart(
        fig_hist, use_container_width=True, key="sales_distribution_histogram"
    )

else:
    st.warning(
        "A total sales or revenue column was not detected. "
        "Your dataset columns are shown below. Check the column names."
    )

# ---------- DATA QUALITY ----------
with st.expander("🧹 Data Quality Summary"):
    quality1, quality2, quality3 = st.columns(3)
    quality1.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
    quality2.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")
    quality3.metric("Columns", len(df.columns))

    st.write("Missing values by column")
    missing = df.isna().sum().rename("Missing Values").to_frame()
    st.dataframe(missing, use_container_width=True)

# ---------- DATA TABLE ----------
st.subheader("📋 Filtered Dataset")
st.caption(f"Showing {len(filtered_df):,} records after applying filters.")
st.dataframe(filtered_df, use_container_width=True)

# ---------- DOWNLOAD ----------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="supermarket_sales_analysis.csv",
    mime="text/csv",
    key="download_filtered_sales"
)
