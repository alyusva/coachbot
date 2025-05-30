from langchain_community.llms import Ollama

def load_model():
        return Ollama(model="mistral")  # usa el modelo local (antes usaba "llama3.2" de Ollama)