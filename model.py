from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter
import torch

MODEL = "llama2"


model = Ollama(model=MODEL)
# Initialize with just the model
embeddings = OllamaEmbeddings(model=MODEL)

# print(model.invoke("Tell me a joke"))


parser = StrOutputParser()
chain = model | parser 

template = """
Match the given vitals of person with good vital range, if given vital are out of range or at extreme ends of good vital range then return, patient is not taking medicines on time, dont add unnecessary information. If you can't answer the question, reply "I don't know". Don't add reference to it.

good vital range:

blood pressure range = 120 >= bp_systolic >= 80 and 80 >= bp_diastolic >= 60
sugar level range = 100 >= sugar level >= 70
pulse rate range = 100 >= pulse rate >= 60
spo2 range = 100 >= spo2_ evel >= 95


Context: f'{context}' 

Question: {question}
"""

prompt = PromptTemplate.from_template(template)
prompt.format(context="Return Yes or No", question="Match Good Vital range with given vitals range in input and return if he is taken medicine or not")

chain = prompt | model | parser

chain = prompt | model | parser

# response = chain.invoke({"context": "Give the details about given medicine", "question": f"{ques}"})

loader = PyPDFLoader("C:\hackX\sodapdf-converted.pdf")
pages = loader.load_and_split()


vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)

retriever = vectorstore.as_retriever()
# r2 = retriever.invoke("Formoterol+ Budesonide MDI,DPI,Rotacap")[0]




# print(f"You have asked about: {question}")
# print(f"Answer: {chain.invoke({'question': question})}")
# print()

chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
    }
    | prompt
    | model
    | parser
)

def response(question):
    return f"Answer: {chain.invoke({'question': question})}"
