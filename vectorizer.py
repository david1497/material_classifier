#%%
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
'sockets': 'Sockets',
'fire stopping': 'Fire Stopping',
'metal': 'Metal',
'plant':'Plant',
'Peter Harper':'Peter Harper', # Should it be in Service Fee?
'Sealant':'Sealant',
'misc':'Misc',
'protection':'Protection',
'firestrip':'Fire Strip',
'vcl' : 'VCL',
'access panels' : 'Access Panels',
'CITB/Training' : 'CITB/Training',
'Insulation': 'Insulation',
'Misc':'Misc',
'QR Codes?':'QR Codes?', # Misc?
'waterproof': 'Waterproof',
'DefHeads & Ply Precuts':'Def Heads&Ply Precuts',
'board' : 'Board',
'Screws':'Screws',
'waste':'Waste',
'logistics':'Logistics',
'steel':'Steel',
'timber': 'Timber',
'ID Cards': 'ID Cards', # Do we have so many to keep it as a cat or we can put it Misc
'purfleet': 'Purfleet',
'VCL':'VCL',
'H&S': 'H&S',
'sealant': 'Sealant',
'Phone Bill' : 'Phone Bill', # Maybe can be service fees
'Tools, Bits, Blades, Etc' : 'Tools, Bits, Blades, etc',
'Finishing (Skim/Joint/Paint etc)': 'Finishing (Skim, Joint, Paint, etc)',
'Service Fee': 'Service Fee',
'unknown': 'Unknown',
'Fixings':'Fixings',
'soffit slab':'Soffit Slab',
'Setout Material': 'Setout Material',
'Internet Order': 'Internet Order'
}

# %%

full_mateirals_df['MainCategory'] = full_mateirals_df['MainCategory'].replace(rename_mapping)
# %%
full_mateirals_df.to_csv('full_material.csv')


# %%
import os, json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

#%%
with open("config.json", 'r') as json_file:
    configs = json.load(json_file)

os.environ["OPENAI_API_KEY"] = configs['secrets']['OPENAI_API_KEY']


embedding_function = OpenAIEmbeddings()

loader = CSVLoader("./full_material.csv")
documents = loader.load()

db = Chroma.from_documents(documents, embedding_function)
retriever = db.as_retriever()


#%%
template = """Given the context:
{context}

Which category should be assigned to: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

#%%

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


#%%
q = """
Cost Code: M232;
Description: BG FireStrip 3600mm (5);
Supplier/Subcontractor: Etag UK;
Src: PL;
Tran Type: PINV; 
Internal Ref: 21110303;
External Ref: 4846 ADZ785;
PO Number: PO001869;
Quantity: 20;
Unit:EA"""


#%%
print(chain.invoke(q))
# %%
