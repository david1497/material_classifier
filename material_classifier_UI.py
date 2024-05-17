import subprocess

# Define the pip command
pip_command = ["pip", "install", "openpyxl"]

# Run the pip command
subprocess.run(pip_command)

import pandas as pd
import streamlit as st

#materials_df = pd.read_csv('https://github.com/david1497/material_classifier/blob/main/unclassified_materials.csv', sep=',')
taxonomy_df = pd.read_excel('https://github.com/david1497/material_classifier/blob/main/taxonomy.xlsx', engine='openpyxl') 

categories = taxonomy_df['Category']
subcategories = ['A', 'B', 'C', 'D', 'E']


def display_row(row):
    st.text(f"Cost Code: {row['Cost Code'].upper()}")
    st.text(f"Description: {row['Description']}")
    st.text(f"Supplier/Subcontractor: {row['Supplier/Subcontractor']}")
    st.text(f"Unit: {row['Unit']}")
    selected_category = st.selectbox(
        "Select the most appropriate category for this material",
        options=categories
    )
    selected_subcategory = st.selectbox(
        "Select the most appropriate SUB category for this material",
        options=subcategories
    )

    return selected_category, selected_subcategory


def main():

    st.text('Material classifier UI')

    idx = st.session_state.get('index', 0)


    # Display row and get user input
    selected_category, selected_subcategory = display_row(materials_df.iloc[idx])

    st.session_state['selected_categories'] = st.session_state.get('selected_categories', [])
    st.session_state['selected_categories'].append(selected_category)
    st.session_state['selected_subcategories'] = st.session_state.get('selected_subcategories', [])
    st.session_state['selected_subcategories'].append(selected_subcategory)


    # Next button to navigate to the next row
    if st.button("Next"):
        idx += 1
        if idx < len(materials_df):
            st.session_state['index'] = idx
        else:
            st.write("End of DataFrame reached. Thank you for your input!")
            st.write("Selected categories:", st.session_state['selected_categories'])


# Run the app
if __name__ == "__main__":
    main()
