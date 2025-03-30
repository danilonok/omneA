from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from configs import llm_config
from llama_index.vector_stores.postgres import PGVectorStore

docs = SimpleDirectoryReader('documents', recursive=True,).load_data()


import psycopg2

connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "RAGDatabase"
conn = psycopg2.connect("dbname='RAGDatabase' user='postgres' host='localhost' password='password'")
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS data_index;')

conn.commit()
conn.close()

connection_string = "RAGDatabase://postgres:password@localhost:5432"

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

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    docs, storage_context=storage_context, show_progress=True
)