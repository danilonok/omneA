from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex
from configs.llm_config import Settings



connection_string = "RAGDatabase://postgres:password@localhost:5432"
db_name = "RAGDatabase"
from sqlalchemy import make_url

url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="index",
    embed_dim=1024,  # openai embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
