import pandas as pd
import streamlit as st

#taxonomy_df = pd.read_csv('./taxonomy.csv', sep=',') 
taxonomy = ["Category",
"ACCESS PANELS",
"BOARD",
"DEF HEADS & PLY PRECUTS",
"DOT/DAB",
"ELECTRICAL COMPONENTS",
"FINISHING",
"FIRE STOPPING",
"FIXINGS AND FASTENERS",
"HEALTH AND SAFETY",
"INSULATION",
"INTERNET ORDER",
"LOGISTICS",
"METAL",
"MISC",
"PLANT",
"PROTECTION",
"SEALANT",
"SERVICE FEE",
"SETOUT MATERIAL",
"SOFFIT SLAB",
"STEEL",
"TIMBER",
"TOOLS AND ACCESSORIES",
"TRAINING",
"UNKNOWN",
"VCL",
"WASTE",
"WATERPROOF"
]
materials_df = pd.read_csv('./unclassified_materials.csv', sep=',')

categories = taxonomy #taxonomy_df['Category']
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
        materials_df.at[idx, 'category'] = selected_category
        materials_df.at[idx, 'subcategory'] = selected_subcategory
        idx += 1
        if idx < len(materials_df):
            st.session_state['index'] = idx
        else:
            st.write("End of DataFrame reached. Thank you for your input!")
            st.write("Selected categories:", st.session_state['selected_categories'])
        materials_df.to_csv('labeled_materials.csv')


# Run the app
if __name__ == "__main__":
    main()
