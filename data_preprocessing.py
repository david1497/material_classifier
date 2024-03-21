#%%
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# %%
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

accruals_file = '/home/vadim/Downloads/PR UK_Cost_Accruals_Transaction_Report_WK.xlsx'
material_file = '/home/vadim/Downloads/Materials Split for Promptloop.xlsx'
full_materials = '/home/vadim/P&R data/All Materials S4 S5 & FR with Catagories FF.xlsx'


#%%

sheets = ['Material Array', 'Data', '21m Screws Check']
temp_list = []
for s in sheets:
    full_materials_pdf = pd.read_excel(full_materials, sheet_name=s)
    main_category = set(full_materials_pdf['MainCategory'])
    print(f"Got it for {s}, total: {len(main_category)}")
    temp_list.append(main_category)
    print(full_materials_pdf[full_materials_pdf['MainCategory']=='Peter Harper'].value_counts())
exploded_list = set([element for subset in temp_list for element in subset])

# %%
accruals_df = pd.read_excel(accruals_file)
accruals_df['supplier'] = accruals_df['Supplier/Subcontractor']
accruals_df.drop(['Record Type', 'Phase', 'Unnamed: 17', 'Unnamed: 15', 'Supplier/Subcontractor'], inplace=True, axis='columns')
accruals_df = accruals_df.dropna(subset=['Description'], axis=0)
accruals_df['simple_supplier_name'] = accruals_df['supplier'].str.split(' - ').str[0]


#%%
def get_wordnet_pos(treebank_tag):
    """get_wordnet_pos

    Sucks

    Args:
        treebank_tag (_type_): _description_

    Returns:
        _type_: _description_
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    


# %%
accruals_df['Description'] = accruals_df['Description'].apply(nltk.word_tokenize)
accruals_df['Description'] = accruals_df['Description'].apply(nltk.pos_tag)

accruals_df['Description'] = accruals_df['Description'].apply(lambda x: [lemmatizer.lemmatize(word, get_wordnet_pos(pos_tag)) for word, pos_tag in x])
accruals_df['Description'] = accruals_df['Description'].apply(' '.join)
# %%

final_list = [
    'Access Panels',
    'Board',
    'CITB/Training',
    'Def Heads&Ply Precuts',
    'Dot/Dab',
    'Finishing (Skim, Joint, Paint, etc)',
    'Fire Stopping',
    'Fire Strip',
    'Fixings',
    'H&S',
    'ID Cards',
    'Insulation',
    'Internet Order',
    'Logistics',
    'Metal',
    'Misc',
    'Overheads',
    'Peter Harper',
    'Phone Bill',
    'Plant',
    'Protection',
    'Purfleet',
    'QR Codes?',
    'Rebate',
    'Screws',
    'Sealant',
    'Service Fee',
    'Setout Material',
    'Sockets',
    'Soffit Slab',
    'Steel',
    'Timber',
    'Tools, Bits, Blades, etc',
    'Unknown',
    'VCL',
    'Waste',
    'Waterproof'
]
#* CamelCase for all material categories, removed Missing since we have Unknown.
#* Unknown may still overlap with the Misc
#* What about Peter Harper? Do we need it as a separate category or we can include that in service fee or Misc
# %%








import pandas as pd

#%%
full_materials = '/home/vadim/P&R data/All Materials S4 S5 & FR with Catagories FF.xlsx'
full_materials_data_df = pd.read_excel(full_materials, sheet_name='Data')
full_materials_screw_df = pd.read_excel(full_materials, sheet_name='Screw Count')

# %%
target_columns = [
    'Cost Code', 
    'Description', 
    'SubCategory', 
    'MainCategory', 
    'Supplier/Subcontractor',
    'Src',
    'Tran Type',
    'Internal Ref', 
    'External Ref', 
    'PO Number', 
    'Quantity',
    'Unit']

full_materials_data_df = full_materials_data_df[target_columns]
full_materials_screw_df = full_materials_screw_df[target_columns]

#%%
full_mateirals_df = pd.concat([full_materials_screw_df, full_materials_data_df], axis='rows')


#%%
rename_mapping = {
    'service fee':'Service Fee',
    'Not Found':'Unknown',
    'Plant':'Plant',
    'Dot / Dab':'Dot/Dab',
    'sockets': 'Electrical Components',#'Sockets',
    'fire stopping': 'Fire Stopping',
    'metal': 'Metal',
    'plant': 'Plant',
    'Peter Harper': 'Service Fee', # Should it be in Service Fee?
    'Sealant': 'Sealant',
    'misc': 'Misc',
    'protection': 'Protection',
    # 'firestrip':'Fire Strip', # should we include it in Fire Stopping?
    'firestrip': 'Fire Stopping',
    'vcl': 'VCL',
    'access panels': 'Access Panels',
    'CITB/Training': 'Training', # is CITB a globally known abbreviation or industry related?
    'Insulation': 'Insulation',
    'Misc': 'Misc',
    # 'QR Codes?':'QR Codes?', # Misc?
    'QR Codes?': 'Misc',
    'waterproof': 'Waterproof',
    'DefHeads & Ply Precuts': 'Def Heads & Ply Precuts',
    'board': 'Board',
    'Screws': 'Fixings and Fasteners',#'Screws',
    'waste': 'Waste',
    'logistics': 'Logistics',
    # 'steel':'Steel', # Can we consider it metal
    'steel':'Metal', # Can we consider it metal
    'timber': 'Timber', # Timber or Wood?
    # 'ID Cards': 'ID Cards', # Do we have so many to keep it as a cat or we can put it Misc
    'ID Cards': 'Misc',
    # 'purfleet': 'Purfleet',
    'purfleet': 'Misc',
    'VCL':'VCL',
    'H&S': 'Health and Safety', #'H&S',
    'sealant': 'Sealant',
    # 'Phone Bill' : 'Phone Bill', # Maybe can be service fees
    'Phone Bill' : 'Service Fee',
    'Tools, Bits, Blades, Etc' : 'Tools and Accessories', #'Tools, Bits, Blades, etc',
    'Finishing (Skim/Joint/Paint etc)': 'Finishing',
    'Service Fee': 'Service Fee',
    'unknown': 'Unknown',
    'Fixings':'Fixings and Fasteners',#'Fixings',
    'soffit slab':'Soffit Slab',
    'Setout Material': 'Setout Material',
    'Internet Order': 'Internet Order'
}

final_list_of_categories = [
    'Access Panels',
    'Board',
    'Def Heads & Ply Precuts',
    'Dot/Dab',
    'Electrical Components',
    'Finishing',
    'Fire Stopping',
    'Fixings and Fasteners',
    'Health and Safety',
    'Insulation',
    'Internet Order',
    'Logistics',
    'Metal',
    'Misc',
    'Plant',
    'Protection',
    'Sealant',
    'Service Fee',
    'Setout Material',
    'Soffit Slab',
    'Timber',
    'Tools and Accessories',
    'Training',
    'Unknown',
    'VCL',
    'Waste',
    'Waterproof'
]

# %%

full_mateirals_df['MainCategory'] = full_mateirals_df['MainCategory'].replace(rename_mapping)
# %%
full_mateirals_df.to_csv('full_material.csv')



#%%
distinct_materials = pd.read_csv('sliced_unclassified_materials.csv')
distinct_materials = distinct_materials.drop_duplicates(subset=['Description'])
distinct_materials = distinct_materials.drop_duplicates(subset=['Supplier/Subcontractor'])
distinct_materials.to_csv('distinct_materials.csv')
# %%
