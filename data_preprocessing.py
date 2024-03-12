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
