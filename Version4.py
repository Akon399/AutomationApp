# import streamlit as st
# import pandas as pd
# import csv

# # Function to detect the delimiter in a CSV file
# def detect_delimiter(file):
#     sniffer = csv.Sniffer()
#     try:
#         sample_bytes = file.read(1024)
#         file.seek(0)  # Reset file pointer to the beginning
#         sample_string = sample_bytes.decode('utf-8')  # Convert bytes to string
#         return sniffer.sniff(sample_string).delimiter
#     except (csv.Error, UnicodeDecodeError):
#         # Default to comma if the sniffer fails
#         return ','

# # Set up the page
# st.set_page_config(page_title='Risk App')
# st.title('Risk Automation App.')
# st.subheader('Upload Merchant Data:')

# # File uploader
# uploaded_file = st.file_uploader('Choose file', type=['csv', 'xlsx'])
# df = pd.DataFrame()  # Initialize an empty DataFrame

# if uploaded_file:
#     st.markdown('---')
    
#     # Check the file type and use the appropriate method to read it
#     if uploaded_file.type == 'application/vnd.ms-excel':  # Check for XLSX file type
#         df = pd.read_excel(uploaded_file, engine='openpyxl')  # Use pd.read_excel for XLSX files
#     else:
#         # Detect the delimiter for CSV files
#         delimiter = detect_delimiter(uploaded_file)
#         try:
#             df = pd.read_csv(uploaded_file, delimiter=delimiter, engine='python', on_bad_lines='skip')
#         except pd.errors.ParserError as e:
#             st.error(f"An error occurred while parsing the CSV file: {e}")
    
#     if df.empty:
#         st.error("The dataset appears empty after processing. Please check if the file is formatted correctly.")
#     else:
#         st.write("Preview of loaded data:")
#         st.dataframe(df.head())  # Show the first few rows as a preview

# # Pivot Table 1
# if not df.empty and st.button("PV1"):
#     st.write("Pivot Table 1: Card Brand vs Status")
#     pivot_table_pv1 = pd.crosstab(df['Card Brand'], df['Status'])
#     st.write(pivot_table_pv1)
    
#     # Add Grand Total column
#     pivot_table_pv1['Grand Total'] = pivot_table_pv1.sum(axis=1)
    
#     # Calculate Acceptance Rate
#     pivot_table_pv1['Acceptance Rate'] = pivot_table_pv1['approved'] / (pivot_table_pv1['Grand Total'] 
#                                                                         - pivot_table_pv1['error'] 
#                                                                         - pivot_table_pv1['refunded'])
    
#     st.write(pivot_table_pv1 * 100)
    
#     # Add a download button for PV1
#     csv_data = pivot_table_pv1.to_csv(index=True, sep=',')
#     st.download_button(
#         label="Download PV1 as CSV",
#         data=csv_data,
#         key="pv1_download",
#         file_name="pivot_table_pv1.csv"
#     )

# # Pivot Table 2
# if not df.empty and st.button("PV2"):
#     st.write("Pivot Table 2: Custom Pivot Table")
    
#     # Create a copy of the DataFrame with the necessary filter
#     filtered_df = df[df['Type'] == 'sale3d']
    
#     # Create a new pivot table
#     pivot_table_pv2 = pd.pivot_table(
#         filtered_df,
#         index=['Merchant', 'ErrorMessage'],
#         values=['Merchant Transaction id'],
#         aggfunc={'Merchant Transaction id': 'count'},
#     )
    
#     # Rename the 'Merchant Transaction ID' column to 'Count of Merchant Transaction ID'
#     pivot_table_pv2.columns = ['Count of Merchant Transaction id']
    
#     # Calculate the Percentage Rate
#     pivot_table_pv2['Percentage Rate'] = (pivot_table_pv2['Count of Merchant Transaction id'] / pivot_table_pv2['Count of Merchant Transaction id'].sum()) * 100
    
#     st.write(pivot_table_pv2)
    
#     # Add a download button for PV2
#     csv_data = pivot_table_pv2.to_csv(index=True, sep=',')
#     st.download_button(
#         label="Download PV2 as CSV",
#         data=csv_data,
#         key="pv2_download",
#         file_name="pivot_table_pv2.csv"
#     )

# # Pivot Table 3
# if not df.empty and st.button("PV3"):
#     st.write("Pivot Table 3: BIN Country vs Status and Transaction id Count")
#     pivot_table_pv3 = df.pivot_table(index='BIN country', columns='Status', values='Transaction id', aggfunc='count', fill_value=0)
#     st.write(pivot_table_pv3)
    
#     # Add a download button for PV3
#     csv_data = pivot_table_pv3.to_csv(index=True, sep=',')
#     st.download_button(
#         label="Download PV3 as CSV",
#         data=csv_data,
#         key="pv3_download",
#         file_name="pivot_table_pv3.csv"
#     )
# ------------------------------------------------------------------------------

import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(page_title='Risk App')
st.title('Automation Application.')
st.subheader('Upload Merchant Data:')

# File uploader
uploaded_file = st.file_uploader('Choose file', type=['csv', 'xlsx'])

# User input for delimiter
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
    
    if df.empty:
        st.error("The dataset appears empty after processing. Please check if the file is formatted correctly.")
    else:
        st.write("Preview of loaded data:")
        st.dataframe(df.head())  # Show the first few rows as a preview
        st.write("Column names in the DataFrame:")
        st.write(df.columns.tolist())  # Display column names

# Pivot Table 1
if not df.empty and st.button("PV1"):
    if 'Card Brand' in df.columns and 'Status' in df.columns:
        st.write("Pivot Table 1: Card Brand vs Status")
        pivot_table_pv1 = pd.crosstab(df['Card Brand'], df['Status'])
        st.write(pivot_table_pv1)
        
        # Additional calculations...
        # Add Grand Total column, Acceptance Rate, etc.

        # Add a download button for PV1
        csv_data = pivot_table_pv1.to_csv(index=True)
        st.download_button(
            label="Download PV1 as CSV",
            data=csv_data,
            file_name="pivot_table_pv1.csv"
        )
    else:
        st.error("Required columns for Pivot Table 1 are not in the DataFrame.")

    # if st.button("PV1"):
            
    #         st.write("Pivot Table 1: Card Brand vs Status")
    #         pivot_table_pv1 = pd.crosstab(df['Card Brand'], df['Status'])
    #         st.write(pivot_table_pv1)
    
    # # Add Grand Total column
    #         pivot_table_pv1['Grand Total'] = pivot_table_pv1.sum(axis=1)
    
    # # Calculate Acceptance Rate
    #         pivot_table_pv1['Acceptance Rate'] = pivot_table_pv1['approved'] / (pivot_table_pv1['Grand Total'] 
    #                                                                     - pivot_table_pv1['error'] 
    #                                                                     - pivot_table_pv1['refunded'])
    
    #         st.write(pivot_table_pv1 * 100)

# Additional Pivot Tables...
# Pivot Table 2, Pivot Table 3, etc., with similar checks as above

