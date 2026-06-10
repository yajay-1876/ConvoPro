from llama_index.core import PromptTemplate

from llm_factory.get_llm import get_ollama_llm

def get_chat_title(model:str, user_query:str):
    llm=get_ollama_llm(model)
    title_prompt_template = f"""
    Generate a title for the following user query.

    Rules:
    - Maximum 4 words
    - No punctuation
    - Return ONLY the title

    User Query:
    {user_query}

    Title:
    """
    title_prompt=PromptTemplate(title_prompt_template).format(user_query=user_query)
    title_=llm.complete(title_prompt).text
    return title_

# Example usage
# print("executing")
# model = "phi3:latest"
# user_query = "Can you explain the concept of reinforcement learning and its applications in modern AI"
# title = get_chat_title(model, user_query)
# print(title)

# NOTE: Smaller models (like gemma 2b) may not give you accurate and short title.