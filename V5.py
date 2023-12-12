import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(page_title='Risk App')
st.title('Risk Automation App.')
st.subheader('Upload Merchant Data:')

# File uploader
uploaded_file = st.file_uploader('Choose file', type=['csv', 'xlsx'])

# User input for delimiter (only for CSV files)
if uploaded_file and uploaded_file.type != 'application/vnd.ms-excel':
    delimiter = st.text_input('Enter delimiter for CSV (default is comma \",\"):', ',')

df = pd.DataFrame()  # Initialize an empty DataFrame

if uploaded_file:
    st.markdown('---')
    
    # Check the file type and use the appropriate method to read it
    if uploaded_file.type == 'application/vnd.ms-excel':  # For XLSX files
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    else:  # For CSV files
        try:
            df = pd.read_csv(uploaded_file, delimiter=delimiter, engine='python')
        except pd.errors.ParserError as e:
            st.error(f"An error occurred while parsing the CSV file: {e}")

    if not df.empty:
        st.write("Preview of loaded data:")
        st.dataframe(df.head())  # Show the first few rows as a preview
        st.write("Column names in the DataFrame:")
        st.write(df.columns.tolist())  # Display column names

# Function to check if required columns exist
def required_columns_exist(columns, dataframe):
    return all(column in dataframe.columns for column in columns)

# Pivot Table 1
if st.button("PV1") and required_columns_exist(['Card Brand', 'Status'], df):
    pivot_table_pv1 = pd.crosstab(df['Card Brand'], df['Status'])
    pivot_table_pv1['Grand Total'] = pivot_table_pv1.sum(axis=1)
    pivot_table_pv1['Acceptance Rate'] = pivot_table_pv1['approved'] / (pivot_table_pv1['Grand Total'] - pivot_table_pv1['error'] - pivot_table_pv1['refunded'])
    st.write(pivot_table_pv1 * 100)
    csv_data = pivot_table_pv1.to_csv(index=True)
    st.download_button(label="Download PV1", data=csv_data, file_name="pivot_table_pv1.csv")

# New Pivot Table 2
if st.button("PV2") and required_columns_exist(['Merchant', 'Merchant Transaction id', 'Amount (with decimal mark per currency exponent)', 'Transaction id'], df):
    # Group by Merchant and calculate required metrics
    pv2_df = pd.DataFrame({
        'Merchant Transaction id': df.groupby('Merchant')['Merchant Transaction id'].nunique(),
        'Amount (with decimal mark per currency exponent)': df.groupby('Merchant')['Amount (with decimal mark per currency exponent)'].sum(),
        'Transaction id %': (df.groupby('Merchant')['Transaction id'].count() / df['Transaction id'].count()) * 100
    }).reset_index()

    st.write(pv2_df)
    csv_data = pv2_df.to_csv(index=False)
    st.download_button(label="Download PV2", data=csv_data, file_name="pivot_table_pv2.csv")


# New Pivot Table 3
if st.button("PV3") and required_columns_exist(['BIN country', 'Status', 'Transaction id', 'Amount (with decimal mark per currency exponent)', 'Merchant Transaction id'], df):
    # Group by BIN country and calculate required metrics
    pv3_df = pd.DataFrame({
        'Merchant Transaction id': df.groupby('BIN country')['Merchant Transaction id'].count(),
        'Amount (with decimal mark per currency exponent)': df.groupby('BIN country')['Amount (with decimal mark per currency exponent)'].sum(),
        'Transaction id': df.groupby('BIN country')['Transaction id'].count(),
    }).reset_index()

    # Calculate Merchant Transaction id %
    pv3_df['Merchant Transaction id %'] = (pv3_df['Transaction id'] / pv3_df['Transaction id'].sum()) * 100

    # Add a row for Grand Total
    grand_total = pv3_df.sum(numeric_only=True).rename('Grand Total')
    pv3_df = pd.concat([pv3_df, grand_total.to_frame().T], ignore_index=True)

    st.write(pv3_df)
    csv_data = pv3_df.to_csv(index=False)
    st.download_button(label="Download PV3", data=csv_data, file_name="pivot_table_pv3.csv")

# Footer with a link
st.markdown("---")
st.markdown('Powered by [emerchantpay.com/](https://www.emerchantpay.com/)')


