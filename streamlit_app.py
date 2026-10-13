
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Supermarket Sales Dashboard",
    layout="wide"
)

st.title("Global Supermarket Sales Analysis")
st.write("Interactive Data Visualization Dashboard")

uploaded_file = st.file_uploader(
    "Upload your supermarket CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Missing Values", int(df.isna().sum().sum()))

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:
        column = st.selectbox(
            "Select a numeric column",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="numeric_histogram"
        )

    category_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if category_columns:
        category = st.selectbox(
            "Select a category column",
            category_columns
        )

        counts = (
            df[category]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        counts.columns = ["Category", "Count"]

        fig = px.pie(
            counts,
            names="Category",
            values="Count",
            title=f"Distribution by {category}",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="category_pie_chart"
        )

else:
    st.info("Upload your CSV file to start the analysis.")
