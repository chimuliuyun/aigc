from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm = Ollama(model="llama2")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{how can langsmith help with testing?}")
])
chain = prompt | llm 
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
chain.invoke({"input": "how can langsmith help with testing?"})