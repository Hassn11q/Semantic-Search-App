import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase_client: Client = create_client(supabase_url, supabase_key)

model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embedding_model = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

def search_papers(query, match_count: int = 6, similarity_threshold: float = 0.75):
    query_embedding = embedding_model.embed_query(query)
    
    response = supabase_client.rpc(
        'vector_search',
        {
            'query_embedding': query_embedding,
            'similarity_threshold': similarity_threshold,
            'match_count': match_count
        }
    ).execute()

    if response.data:
        return response.data
    else:
        return []

def get_recent_papers(limit: int = 10):
    response = supabase_client.table("research_papers").select("*").order('published_date', desc=True).limit(limit).execute()
    return response.data if response.data else []

def get_paper_by_title(title: str):
    response = supabase_client.table("research_papers").select("*").eq('title', title).execute()
    return response.data[0] if response.data else None