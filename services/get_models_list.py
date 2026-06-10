from config.settings import Settings

settings=Settings()

def get_ollama_models_list():
    models_str=settings.CONVOPRO_OLLAMA_MODELS
    ollama_models_list=[ model.strip() for model in models_str.split(",") if model.strip()]
    return ollama_models_list

# Example usage
# check_ollama_models = get_ollama_models_list()
# print(type(check_ollama_models))   # <class 'list'>
# print(check_ollama_models)         # ['qwen3:4b', 'qwen3:4b', 'llama3:latest']
