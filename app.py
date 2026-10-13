
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Global Supermarket Sales Analysis")
st.write("Enter supermarket transaction details to analyze sales.")

# Store entered records during the session
if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

# User input form
st.sidebar.header("Enter Sales Details")

with st.sidebar.form("sales_form"):
    city = st.selectbox(
        "Select City",
        ["Yangon", "Mandalay", "Naypyitaw", "Other"]
    )

    if city == "Other":
        city = st.text_input("Enter City Name")

    customer_type = st.selectbox(
        "Customer Type",
        ["Member", "Normal"]
    )

    gender = st.selectbox(
        "Gender",
        ["Female", "Male", "Prefer not to say"]
    )

    category = st.selectbox(
        "Product Category",
        [
            "Food and Beverages",
            "Fashion Accessories",
            "Electronic Accessories",
            "Home and Lifestyle",
            "Sports and Travel",
            "Health and Beauty"
        ]
    )

    payment = st.selectbox(
        "Payment Method",
        ["Cash", "Credit Card", "E-wallet"]
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=1000,
        value=1
    )

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.01,
        value=100.00,
        step=10.0
    )

    tax_rate = st.number_input(
        "Tax Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5
    )

    submitted = st.form_submit_button("Add Sales Record")

    if submitted:
        if city.strip():
            subtotal = quantity * unit_price
            tax = subtotal * tax_rate / 100
            total = subtotal + tax

            st.session_state.sales_data.append({
                "City": city,
                "Customer Type": customer_type,
                "Gender": gender,
                "Product Category": category,
                "Payment Method": payment,
                "Quantity": quantity,
                "Unit Price": unit_price,
                "Subtotal": round(subtotal, 2),
                "Tax": round(tax, 2),
                "Total Sales": round(total, 2)
            })

            st.sidebar.success("Sales record added!")
        else:
            st.sidebar.error("Please enter a city name.")

# Dashboard
if st.session_state.sales_data:
    df = pd.DataFrame(st.session_state.sales_data)

    st.subheader("📊 Sales Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", len(df))
    col2.metric("Total Sales", f"{df['Total Sales'].sum():,.2f}")
    col3.metric("Total Quantity", int(df["Quantity"].sum()))
    col4.metric("Average Transaction", f"{df['Total Sales'].mean():,.2f}")

    st.divider()

    # City sales bar chart
    st.subheader("Sales by City")
    city_sales = (
        df.groupby("City", as_index=False)["Total Sales"]
        .sum()
    )

    fig1 = px.bar(
        city_sales,
        x="City",
        y="Total Sales",
        color="City",
        title="Total Sales by City",
        text_auto=".2f"
    )
    st.plotly_chart(fig1, use_container_width=True, key="city_sales_chart")

    # Category pie chart
    st.subheader("Sales by Product Category")
    category_sales = (
        df.groupby("Product Category", as_index=False)["Total Sales"]
        .sum()
    )

    fig2 = px.pie(
        category_sales,
        names="Product Category",
        values="Total Sales",
        hole=0.4,
        title="Sales Distribution by Category"
    )
    st.plotly_chart(fig2, use_container_width=True, key="category_sales_chart")

    # Payment method chart
    st.subheader("Payment Method Analysis")
    payment_sales = (
        df.groupby("Payment Method", as_index=False)["Total Sales"]
        .sum()
    )

    fig3 = px.bar(
        payment_sales,
        x="Payment Method",
        y="Total Sales",
        color="Payment Method",
        title="Sales by Payment Method"
    )
    st.plotly_chart(fig3, use_container_width=True, key="payment_sales_chart")

    # Customer type analysis
    st.subheader("Customer Type Analysis")
    customer_sales = (
        df.groupby("Customer Type", as_index=False)["Total Sales"]
        .sum()
    )

    fig4 = px.pie(
        customer_sales,
        names="Customer Type",
        values="Total Sales",
        title="Member vs Normal Customer Sales"
    )
    st.plotly_chart(fig4, use_container_width=True, key="customer_sales_chart")

    # Data table
    st.subheader("All Entered Sales Records")
    st.dataframe(df, use_container_width=True)

    # Download records
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Sales Data as CSV",
        data=csv,
        file_name="supermarket_sales.csv",
        mime="text/csv"
    )

    if st.button("Clear All Records"):
        st.session_state.sales_data = []
        st.rerun()

else:
    st.info("Enter sales details in the left sidebar and click Add Sales Record.")
    st.write("Your dashboard charts will appear after you add the first record.")
