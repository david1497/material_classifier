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
