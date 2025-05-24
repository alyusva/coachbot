from langchain_community.llms import Ollama

def load_model():
        return Ollama(model="llama3.2")  # usa el modelo local ya descargado