#%%
import os
import json
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import langchain
from langchain.llms import OpenAI
import chromadb
from langchain.agents import AgentType, initialize_agent, load_tools


#%%
import serpapi
# from serpapi import GoogleSearch

#%%
params = {
  "engine": "google",
  "q": "Fresh Bagels",
  "location": "Seattle-Tacoma, WA, Washington, United States",
  "hl": "en",
  "gl": "us",
  "google_domain": "google.com",
  "num": "10",
  "start": "10",
  "safe": "active",
  "api_key": "bda83714bab8ce2865270b80648e537bb290016ac73eeb8113ba22cd9907dee4"
}


search = serpapi.search(params)
# results = search.get_dict()
# organic_results = results["organic_results"]

#%%

#* consider the following tools to use with LangChain:
#* The Home Depot API 
#* Walmart Search Engine Results API
#* Google Shopping API
#* Google Product API
#* Ebay Search Engine Results API
#*
# %%
with open("config.json", 'r') as json_file:
    configs = json.load(json_file)

os.environ["OPENAI_API_KEY"] = configs['secrets']['OPENAI_API_KEY']
os.environ["HUGGINGFACEHUB_API_TOKEN"] = configs['secrets']['HUGGING_FACE_TOKEN']
os.environ["SERPAPI_API_KEY"] = configs['secrets']['SERPAPI_KEY']

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="material_classification")

#%%
llm = HuggingFaceHub(
    repo_id="timpal0l/mdeberta-v3-base-squad2")


#%%
tools = load_tools(['serpapi'], llm=llm)


#%%
agent = initialize_agent(
    tools, 
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    handle_parsing_errors=True,
    verbose=True
    )

# %%
prompt_template_binary = PromptTemplate(
    input_variables = ['material_description', 'material_categories'],
    template = "I want to know if the provided material description:\n{material_description};\nis sufficient to classify the material in one of the following categories: {material_categories}. Please respond yes or no."
)


# %%
p = prompt_template_binary.format(
    material_description='Site Secure Chest 4 x 4 x 2',
    material_categories=material_categories)
print(p)



# %%
material_description = 'Board 3x4 oak'

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate.from_template("Given the following material categories {material_categories}, please classify the '{material_description}'")
# prompt.format(material_categories=material_categories, material_description=material_description)
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
response = chain.run(material_categories=material_categories, material_description=material_description)
print(response)



#%%
from transformers import pipeline

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
material_description = 'Drill Bit SDS Plus 5.5x160'

# %%
# import torch


qa_model = pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2")
question = f"How should {material_description} be classified?"
context = f"Given the following material categories {final_list}"
qa_model(question = question, context = context)
# {'score': 0.975547730922699, 'start': 28, 'end': 36, 'answer': ' Sweden.'}

# %%

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

classifier(material_description, final_list)
# %%
