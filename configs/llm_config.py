from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from llama_index.core import Settings

HOST = 'https://9f22-109-86-225-99.ngrok-free.app'
Settings.llm = Ollama(model="qwen2.5:14b", base_url=HOST,request_timeout=60.0)
Settings.embed_model = OllamaEmbedding(model_name="mxbai-embed-large", base_url=HOST, request_timeout=60.0)