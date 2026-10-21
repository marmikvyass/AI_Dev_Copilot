from langchain_groq import ChatGroq
from core.config import settings
from dotenv import load_dotenv

load_dotenv()

class LLM_Generate:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise  ValueError('Groq API Key not Fount')

        self.llm = ChatGroq(
            model='openai/gpt-oss-120b',
            api_key=settings.GROQ_API_KEY,
            temperature=1
        )


    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content