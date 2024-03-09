#%%
import pandas as pd

# %%
accruals_file = '/home/vadim/Downloads/PR UK_Cost_Accruals_Transaction_Report_WK.xlsx'
material_file = '/home/vadim/Downloads/Materials Split for Promptloop.xlsx'


# %%
accruals_df = pd.read_excel(accruals_file)
accruals_df['supplier'] = accruals_df['Supplier/Subcontractor']
accruals_df.drop(['Record Type', 'Phase', 'Unnamed: 17', 'Unnamed: 15', 'Supplier/Subcontractor'], inplace=True, axis='columns')
accruals_df = accruals_df.dropna(subset=['Description'], axis=0)
accruals_df['simple_supplier_name'] = accruals_df['supplier'].str.split(' - ').str[0]

# materials_df = pd.read_excel(material_file)


# %%
suppliers_df = accruals_df['supplier'].value_counts().reset_index()
# remove the - from the supplier name
suppliers_df['simple_name'] = suppliers_df['supplier'].str.split(' - ').str[0]


# %%
def get_top_n(supplier, top_n=False):

    if isinstance(supplier, list):
        df = accruals_df[accruals_df['supplier'].isin(supplier)]['Description'].value_counts().reset_index()
    else:
        df = accruals_df[accruals_df['supplier'].str.contains(supplier)]['Description'].value_counts().reset_index()

    if top_n:
        return df.head(top_n)
    else:
        return df
# %%
# Remove trainings
# Check description with very short name; label those
# Products with description M, P
# What is CCF - 10..?
# CCF - 1055 has 780 products out of which there are only 3 ditinct ones
# SAS International SetUp charge and Delivery charge can be excluded
# Online orders is a bit of a mess
# What is the difference between Encon Insulation Ltd Main Account and Encon Insulation Ltd - 1078
# I assume the numbers after the - is the supplier number. Which if removed, can help join several suppliers
    
#* Split the description into words, lowercase and get a count by words in the description
#* Many elements may have same name even though the suppliers is the same
#* 10% of the data contains NA in description (6003)
#* accruals_df['Description'].isna().sum()
#* Remove trailling spaces at the end of the supplier name
#*    [Penlaw, Encon, Gridline Construction, Keyman Personnel, Minister]
#* All recruitment companies
#* Employees that are contractors

# What is the difference between so many Penlaw suppliers? []
suppliers_df['simple_name_'] = suppliers_df['simple_name'].str.replace()