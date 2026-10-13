# Supermarketsales
# Interactive Data Visualization Dashboard for Global Supermarket Sales Analysis

## 👥 Project Team

This is a group project developed as part of our Data Visualization coursework.

| S.No. | Team Member Name | Roll Number |
|       |                  |             |
| 1     | K. Manasa        | [         ] |

## Project Guide

Guide Name: Dr. B. Mahesh

## Department

Computer Science and Engineering (Artificial Intelligence)

## Project Overview

This Data Visualization project explores global supermarket sales data using Python, Pandas, Plotly, and Streamlit. The project analyzes sales performance, product categories, customer purchasing patterns, payment methods, and city-wise sales trends through an interactive dashboard.

Users can upload a supermarket sales CSV file, apply filters, view key performance indicators, and explore visualizations to understand sales performance and identify useful business insights.

## Visualizations

1. Overall Supermarket Sales Performance
2. City-wise Sales Comparison
3. Product Category-wise Sales Analysis
4. Sales Contribution by Product Category
5. Monthly Sales Trends
6. Customer Type-wise Sales Analysis
7. Payment Method Distribution
8. Quantity Sold and Sales Performance
9. Distribution of Sales Values
10. Interactive Filtering and Data Exploration

The dashboard also provides summary statistics, a filtered dataset preview, data quality information, and an option to download the filtered data as a CSV file.

## Dataset

The project uses a supermarket sales dataset in CSV format, which can be obtained from Kaggle or another suitable data source.

The dataset may contain information such as invoice ID, branch, city, customer type, gender, product line, unit price, quantity, tax, total sales, date, time, payment method, and customer rating.

The application allows users to upload their own supermarket sales CSV file. The uploaded data is processed and analyzed to generate relevant charts, summary statistics, and interactive visualizations.

## Requirements

- Python 3.9 or newer
- Streamlit
- Pandas
- NumPy
- Plotly

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

1. Download or clone the project repository from GitHub.
2. Make sure `app.py` and `requirements.txt` are available in the project folder.
3. Install the required Python dependencies.
4. Run the Streamlit application:

```bash
streamlit run app.py
```

5. Open the local URL displayed in the terminal.
6. Upload the supermarket sales CSV file using the file uploader.
7. Apply the available filters, such as city, product category, customer type, and payment method.
8. Explore the interactive charts, sales summaries, and analysis results.

The dashboard can also be deployed using Streamlit Community Cloud by connecting the GitHub repository.

## DASHBOARD LINK

[https://supermarketsales-ljvha9itwikwisvdjrrd3d.streamlit.app/]

## Important Data Note

The quality and accuracy of the analysis depend on the uploaded dataset's completeness, column names, date formats, and data types. Missing values, duplicate records, inconsistent categories, and invalid numerical values may affect the results.

Sales totals and other performance indicators should be interpreted according to the dataset's definitions and coverage. This project provides exploratory data analysis and visual insights; its findings should not automatically be treated as evidence of business performance beyond the available data.
