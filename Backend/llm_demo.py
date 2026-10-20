from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv
import streamlit as st

load_dotenv()



llm = HuggingFacePipeline.from_model_id(
    model_id='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    task='text-generation'
)

model = ChatHuggingFace(
    llm=llm
)
st.header('Reasearch Tool')
user_input = st.text_input('Enter your prompt')

if st.button('Summerize'):
    res = model.invoke(user_input)
    st.write(res.content)

