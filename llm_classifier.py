#%%
import os
import json
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import langchain

#* consider the following tools to use with LangChain:
#* The Home Depot API 
#* Walmart Search Engine Results API
#* Google Shopping API
#* Google Product API
#* Ebay Search Engine Results API
#*

#%%

from langchain.agents import AgentType, initialize_agent, load_tools

# %%
with open("config.json", 'r') as json_file:
    configs = json.load(json_file)

os.environ["OPENAI_API_KEY"] = configs['secrets']['OPENAI_API_KEY']
os.environ["HUGGINGFACEHUB_API_TOKEN"] = configs['secrets']['HUGGING_FACE_TOKEN']
os.environ["SERPAPI_API_KEY"] = configs['secrets']['SERPAPI_KEY']

material_categories = [
    'Concrete and Cement Products',
    'Steel and Metal Products',
    'Wood and Timber Products',
    'Electrical and Wiring Components',
    'Plumbing and Pipe Fittings',
    'Insulation and Sealants',
    'Roofing Materials',
    'Flooring and Tiles',
    'Paints and Coatings',
    'Windows and Doors',
    'Fixtures and Fittings',
    'HVAC (Heating, Ventilation, and Air Conditioning) Systems',
    'Masonry and Brickwork Materials',
    'Landscaping and Outdoor Supplies',
    'Safety Equipment and Personal Protective Gear'
]

#%%
llm = HuggingFaceHub(repo_id="facebook/nllb-200-distilled-600M",
                     model_kwargs={"temperature":0.1, "max_length":64, "src_lang":'English', "tgt_lang":"Finnish"})


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
material_description = 'Site Secure Chest 4 x 4 x 2'
query = f"Given the following material categories {material_categories}, please classify the '{material_description}'"
agent.run(query)
# %%
