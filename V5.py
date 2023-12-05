import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(page_title='Risk App')
st.title('Risk Automation Application.')
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

# Pivot Table 2
if st.button("PV2") and required_columns_exist(['Type', 'Merchant', 'ErrorMessage', 'Merchant Transaction id'], df):
    # Extract the last 4 digits from the 'Merchant' column
    df['Merchant Group'] = df['Merchant'].str.extract(r'(.+? - \d{4})$')

    # Group by the merchant group and error message, then count occurrences
    pivot_table_pv2 = df[df['Type'] == 'sale3d'].groupby(['Merchant Group', 'ErrorMessage']).size().reset_index(name='Count of Merchant Transaction id')

    # Calculate Percentage Rate
    total_counts = pivot_table_pv2.groupby('Merchant Group')['Count of Merchant Transaction id'].sum().reset_index()
    pivot_table_pv2 = pivot_table_pv2.merge(total_counts, on='Merchant Group', suffixes=('', '_total'))
    pivot_table_pv2['Percentage Rate'] = (pivot_table_pv2['Count of Merchant Transaction id'] / pivot_table_pv2['Count of Merchant Transaction id_total']) * 100

    # Remove duplicates in 'Merchant Group' to make it unique
    pivot_table_pv2 = pivot_table_pv2.drop_duplicates(subset='Merchant Group', keep='first')

    st.write(pivot_table_pv2.drop('Count of Merchant Transaction id_total', axis=1))
    csv_data = pivot_table_pv2.drop('Count of Merchant Transaction id_total', axis=1).to_csv(index=False)
    st.download_button(label="Download PV2", data=csv_data, file_name="pivot_table_pv2.csv")


# Pivot Table 3
if st.button("PV3") and required_columns_exist(['BIN country', 'Status', 'Transaction id'], df):
    pivot_table_pv3 = df.pivot_table(index='BIN country', columns='Status', values='Transaction id', aggfunc='count', fill_value=0)
    st.write(pivot_table_pv3)
    csv_data = pivot_table_pv3.to_csv(index=True)
    st.download_button(label="Download PV3", data=csv_data, file_name="pivot_table_pv3.csv")

# Footer with a link
st.markdown("---")
st.markdown('Powered by [emerchantpay.com/](https://www.emerchantpay.com/)')


