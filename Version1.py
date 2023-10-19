import streamlit as st
import pandas as pd

st.set_page_config(page_title='Risk App')
st.title('Risk Automation App.')
st.subheader('Upload Merchant Data:')

uploaded_file = st.file_uploader('Choose file', type='csv')
if uploaded_file:
    st.markdown('---')
    df = pd.read_csv(uploaded_file, engine='python')
    st.dataframe(df)

if st.button("PV1"):
    st.write("Pivot Table 1: Card Brand vs Status")
    pivot_table_pv1 = pd.crosstab(df['Card Brand'], df['Status'])
    st.write(pivot_table_pv1)
    
    # Add Grand Total column
    pivot_table_pv1['Grand Total'] = pivot_table_pv1.sum(axis=1)
    
    # Calculate Acceptance Rate
    pivot_table_pv1['Acceptance Rate'] = pivot_table_pv1['approved'] / (pivot_table_pv1['Grand Total'] 
                                                                        - pivot_table_pv1['error'] 
                                                                        - pivot_table_pv1['refunded'])
    
    st.write(pivot_table_pv1 * 100)
    
    # Add a download button for PV1
    csv = pivot_table_pv1.to_csv(index=True)
    st.download_button(
        label="Download PV1 as CSV",
        data=csv,
        key="pv1_download",
        file_name="pivot_table_pv1.csv"
    )

if st.button("PV2"):
    st.write("Pivot Table 2: Custom Pivot Table")
    
    # Create a copy of the DataFrame with the necessary filter
    filtered_df = df[df['Type'] == 'sale3d']
    
    # Create a new pivot table
    pivot_table_pv2 = pd.pivot_table(
        filtered_df,
        index=['Merchant', 'ErrorMessage'],
        values=['Merchant Transaction id'],
        aggfunc={'Merchant Transaction id': 'count'},
    )
    
    # Rename the 'Merchant Transaction ID' column to 'Count of Merchant Transaction ID'
    pivot_table_pv2.columns = ['Count of Merchant Transaction id']
    
    # Calculate the Percentage Rate
    pivot_table_pv2['Percentage Rate'] = (pivot_table_pv2['Count of Merchant Transaction id'] / pivot_table_pv2['Count of Merchant Transaction id'].sum()) * 100
    
    st.write(pivot_table_pv2)
    
    # Add a download button for PV2
    csv = pivot_table_pv2.to_csv(index=True)
    st.download_button(
        label="Download PV2 as CSV",
        data=csv,
        key="pv2_download",
        file_name="pivot_table_pv2.csv"
    )

if st.button("PV3"):
    st.write("Pivot Table 3: BIN Country vs Status and Transaction id Count")
    pivot_table_pv3 = df.pivot_table(index='BIN country', columns='Status', values='Transaction id', aggfunc='count', fill_value=0)
    st.write(pivot_table_pv3)
    
    # Add a download button for PV3
    csv = pivot_table_pv3.to_csv(index=True)
    st.download_button(
        label="Download PV3 as CSV",
        data=csv,
        key="pv3_download",
        file_name="pivot_table_pv3.csv"
    )

