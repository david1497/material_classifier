#%%
import pandas as pd
import streamlit as st
import os
from llm_model import build_chain



#%%
input_file = st.file_uploader(label='Add your input file', type=['csv', 'xlsx', 'xls'], accept_multiple_files=False)

if input_file is not None:
    # Get the file name
    file_name = input_file.name
    
    # Extract the file extension
    file_extension = os.path.splitext(file_name)[1]

    if file_extension == '.xlsx':

        file_sheets = pd.ExcelFile(input_file).sheet_names

        if len(file_sheets) > 1:
            
            st.info('You have more than one sheet in your excel. Please choose the one')

            sheet_name = st.selectbox(
                label="Please choose the sheet name", 
                options=file_sheets,
                placeholder=file_sheets[0])
            
            file_content = pd.read_excel(input_file, sheet_name=sheet_name)
    
    elif file_extension == '.csv':

        file_content = pd.read_csv(input_file)

    else:

        st.text('Sorry buddy - wrong file format.')
    
    file_columns = list(file_content.columns)

    st.dataframe(file_content.head(2))

    focus_columns = st.multiselect(
        label='Please choose the input columns', 
        options=file_columns,
        default=file_columns[0],
        placeholder='Choose the input columns')
    st.text(focus_columns)

    focus_df = file_content[focus_columns]
    st.dataframe(focus_df.head(10))

    output_labels = st.text_area(label='Paste the categories you want to get as outcome', 
                 placeholder="['category1','category2','category3','category4']")
    

    output = []
    st.text(focus_df.columns)

    for index, row in focus_df.head(20).iterrows():
        # st.text(row)
        material_characterisitcs = f"""
        Cost Code: {row['Cost Code']};
        Description: {row['Description']};
        Supplier/Subcontractor: {row['Supplier/Subcontractor']};
        Src: {row['Src']};
        Tran Type: {row['Tran Type']}; 
        Internal Ref: {row['Internal Ref']};
        External Ref: {row['External Ref']};
        Quantity: {row['Quantity']};
        Unit: {row['MeasureUnit']}""" 
        chain = build_chain()
        label = chain.invoke(material_characterisitcs)
        st.text(row)
        st.text(f">->->->-> {label}")

        # output.append([row, label])



