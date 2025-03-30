from llama_index.core.prompts import PromptTemplate

DEFAULT_COMPLETION_PROMPT_TMPL = (
    "You are an Windows PC Assistant. Answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)
default_completion_prompt = PromptTemplate(DEFAULT_COMPLETION_PROMPT_TMPL)