# Sales Dashboard
This sales dashboard is built using Streamlit, a popular python library for building interactive web applications. The\
dashboard allows you to filter and explore a electronics sales dataset, and visualize key performance metrics, sales by product\
type overtime, sales by product type and gender, top customers and products and total sales by product type.
## Prerequisites
To run this dashboard, you need to have Python 3.0 or later installed on your computer, as well as the following libraries:
* Pandas
* Streamlit
* Plotly Express

## How to use
1. Download the Electronic_sales_Sep2023-Sep2024.csv file and put it in the data folder
2. Run the script in your terminal or command prompt: streamlit run app.py
3. The dashboard will open in your web browser. You can use the filters on the sidebar to explre the dataset and\
visualize the metrics and charts
## Features

### Filters
The sidebar of the dashoboard includes four filters that allow you to filter the dataset:
* Date range filter: choose a start and end date to filter by the order date.
* Product type filter: select one or more product types to filter by.
* Payment method filter: select one or more payment types to filter by.
* Order status filter: select one or more statuses to filter by.
### KPI Metrics
* Total sales
* Total number of orders
* Average order value
* Number of unique customers
### Sales Over time
This chart display the total sales by product type over time. You can hover over the chart to see the details for a\
specific date and product type.
### Sales by Product Type and Gender
This chart displays the total sales by product type and gender. 
### Distribution of Shipping Types
This chart disaplys the number of orders by shipping method.
### Top 10 Cusomter, Products, and Total Sales by Product Types
These tables display the top 10 customers, products and total sales by product type and top payment methods for the filtered dataset.
