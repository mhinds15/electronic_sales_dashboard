import pandas as pd
import streamlit as st
import plotly.express as px

from typing import List, Tuple

def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

# Load the CSV file
st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv("data/Electronic_sales_Sep2023-Sep2024.csv", parse_dates=["Purchase Date"])
    data["Purchase Date"] = pd.to_datetime(data["Purchase Date"])

    # Correct null value
    data.loc[data["Customer ID"]== 19998, "Gender"] = "Male"

    # Correct duplicate payment methods
    data["Payment Method"]=data["Payment Method"].replace("PayPal", "Paypal")
    return data

#df = load_data()

def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    return data[data[column].isin(values)] if values else data

def calculate_kpi(data: pd.DataFrame):
    total_sales = data["Total Price"].sum()
    sales_in_m = f"{total_sales / 1000000:.2f}M"
    total_orders = data["Customer ID"].nunique()
    average_sales_per_order = f"{total_sales / total_orders / 1000:.2f}K"
    unique_customers = data["Customer ID"].nunique()
    return [sales_in_m, total_orders, average_sales_per_order, unique_customers]
#Filters

def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(4), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value)

def display_sidebar(data: pd.DataFrame):
    st.sidebar.header("Filter Options")
    start_date = pd.Timestamp(st.sidebar.date_input("Start date", data["Purchase Date"].min().date()))
    end_date =  pd.Timestamp(st.sidebar.date_input("End date", data["Purchase Date"].max().date()))
    
    product_types = sorted(data["Product Type"].unique())
    selected_product_types = st.sidebar.multiselect("Product Type(s)", product_types, product_types)

    selected_payment_methods = st.sidebar.multiselect("Select Payment Method", data["Payment Method"].unique())

    selected_order_status = st.sidebar.multiselect("Select Order Status", data["Order Status"].unique())

    st.sidebar.info("Created by Myles Hinds")

    return selected_product_types, selected_payment_methods, selected_order_status

def display_charts(data: pd.DataFrame):
    combine_product_types = st.checkbox("Combine Product Types", value=True)

    if combine_product_types:
        fig = px.area(data, x = "Purchase Date", y="Total Price", color="Product Type",
                      title="Sales over time by Product Type", width=900, height=500)
    else:
        fig = px.area(data, x = "Purchase Date", y="Total Price", color="Product Type",
                      title="Sales over time by Product Type", width=900, height=500) 

    fig.update_layout(margin=dict(l=20, r=20,t=50,b=20)) 
    fig.update_xaxes(rangemode="tozero", showgrid=False)
    fig.update_yaxes(rangemode="tozero", showgrid=True)

    product_type_by_gender = data.groupby(["Product Type", "Gender"])["Total Price"].sum().reset_index()

    fig2 = px.bar(
        product_type_by_gender,
        x="Product Type", y="Total Price", color="Gender", barmode="group",
        title="Sales by Product Type and Gender", text="Total Price"
    )

    shipping_method = data["Shipping Type"].value_counts().reset_index()
    shipping_method.columns = ["Shipping Type", "Count"]

    fig3 = px.bar(
        shipping_method,
        x="Shipping Type", y="Count", color="Shipping Type",
        title="Distribution of Shipping Types", text="Count",  width=900, height=500
    )

     

    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Top 10 Customers")
        top_customers = data.groupby("Customer ID")["Total Price"].sum().reset_index().sort_values("Total Price", ascending=False).head(10)

        st.write(top_customers)
    with col2:
        st.subheader("Total Sales by Product Type")
        total_sales_by_product_type = data.groupby("Product Type")["Total Price"].sum().reset_index()
        st.write(total_sales_by_product_type)

    with col3:
        st.subheader("Total Sales by Payment Method")
        total_sales_by_payment_method = data.groupby("Payment Method")["Total Price"].sum().reset_index()
        st.write(total_sales_by_payment_method)


def main():
    #set_page_config()

    data = load_data()

    st.title("Electronics Sales Dashboard")

    selected_product_types, selected_payment_method, selected_order_status = display_sidebar(data)

    filtered_data = data.copy()
    filtered_data = filter_data(filtered_data, "Product Type", selected_product_types)
    filtered_data = filter_data(filtered_data, "Payment Method", selected_payment_method)
    filtered_data = filter_data(filtered_data, "Order Status", selected_order_status)

    kpis = calculate_kpi(filtered_data)
    kpi_names = ["Total Sales", "Total Orders", "Average Sales per Order", "Unique Customers"]
    display_kpi_metrics(kpis, kpi_names)

    display_charts(filtered_data)

if __name__=='__main__':
    main()


