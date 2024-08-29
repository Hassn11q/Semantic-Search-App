# Import required libraries 
import arxiv 
import datetime
import pytz 
import pandas as pd 
import os 
from dotenv import load_dotenv 
from supabase import Client, create_client 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

# Load env keys
groq_api = os.getenv('GROQ_API_KEY')
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase_client = create_client(supabase_url, supabase_key)

# Initialize arxiv client
client = arxiv.Client()

# Keywords to search for
keyword = ['rag', "large language models", "retrieval augmented generation"]
search = arxiv.Search(
    query=keyword[1],
    max_results=30, 
    sort_by=arxiv.SortCriterion.SubmittedDate, 
    sort_order=arxiv.SortOrder.Descending
)

results = client.results(search)
papers = list(results)

# Filter papers from the last 7 days
utc = pytz.timezone("UTC")
current_datetime = datetime.datetime.now(utc)
seven_days_ago = current_datetime - datetime.timedelta(days=7)
papers_of_this_week = [paper for paper in papers if paper.published >= seven_days_ago]

# Initialize  LLM
llm_name ="llama-3.1-70b-versatile"
llm = ChatGroq(model="llama-3.1-70b-versatile" ,  groq_api_key= groq_api)

# Initialize  Embeddings
model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embedding = HuggingFaceEmbeddings(model_name = model_name, model_kwargs = model_kwargs, encode_kwargs =encode_kwargs )

# Define the schema for extraction
class Extract(BaseModel):
    problem: str = Field(description="Extract the main research problem from the abstract")
    solution: str = Field(description="Extract the proposed method, approach, or solution from the abstract. Be concise, specific, and highly accurate")
    result: str = Field(description="A summary of the main findings or outcomes derived from applying the proposed solution")

parser = JsonOutputParser(pydantic_object=Extract)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

# Process each paper and insert it into the Supabase table
for i in range(len(papers_of_this_week)):
    try:
        result = chain.invoke({"query":papers_of_this_week[i].summary})
        result['author'] = ",".join([author.name for author in papers_of_this_week[i].authors])
        result['url'] = next((link.href for link in papers_of_this_week[i].links if link.title == "pdf") , None)
        result['embedding'] = embedding.embed_query(result['solution'])
        result['title'] = papers_of_this_week[i].title
        result['published_date'] = pd.Timestamp(papers_of_this_week[i].published).strftime("%Y-%m-%d_%H:%M:%S")
        supabase_client.table("research_papers").upsert(result , returning="minimal" , on_conflict="title").execute()
        print(f"Successfully inserted paper: {papers_of_this_week[i].title}")
    except Exception as e:
        print(f"Failed to insert paper: {papers_of_this_week[i].title}. Error: {str(e)}")

# Define the log file 
log_file = "log.txt"

# Get the current date and time
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create the log entry
log_entry = f"{current_datetime}: Successfully inserted paper: {papers_of_this_week[i].title}\n"

# Write the log entry to the log file
with open(log_file, 'a') as file:
    file.write(log_entry)
print(f"Log entry added: {log_entry}")
