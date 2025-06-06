from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex
from configs.llm_config import Settings

import json


with open('core/few_shot_prompt_enrichment/steps.json', 'r') as openfile:
    json_object = json.load(openfile)


nodes = []
for pair in json_object['pairs']:
    node = TextNode(text=pair['query'], metadata={'steps': pair['steps']})
    nodes.append(node)

vector_index = VectorStoreIndex(nodes=nodes)

retriever = vector_index.as_retriever(
    similarity_top_k=3
)

