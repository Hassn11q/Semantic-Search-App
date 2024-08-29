import os
from dotenv import load_dotenv
from supabase import Client, create_client
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Load env keys
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase_client: Client = create_client(supabase_url, supabase_key)

# Initialize Embeddings
model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embedding = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

def search_papers(query):
    query_embedding = embedding.embed_query(query)
    
    # Perform the search using Supabase's vector similarity search
    params = {
        'query_embedding': query_embedding,
        'similarity_threshold': 0.75,
        'match_count': 6
    }
    response = supabase_client.rpc('vector_search', params).execute()
    
    return response.data

