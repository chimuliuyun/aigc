# 导入Ollama模型和ChatPromptTemplate模板
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
# 导入StrOutputParser解析器
from langchain_core.output_parsers import StrOutputParser
# 创建Ollama模型实例
llm = Ollama(model="llama2")

# 创建ChatPromptTemplate模板实例
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

# 创建StrOutputParser解析器实例
output_parser = StrOutputParser()

# 将模板、模型和解析器实例连接起来
chain = prompt | llm | output_parser

# 调用链，传入输入参数
chain.invoke({"input": "how can langsmith help with testing?"})

# 打印结果
result = chain.invoke({"input": "how can langsmith help with testing?"})
print(result)
# print(llm)
# print(llm.generate([prompt.format(input="how can langsmith help with testing?")]))
# print(output_parser.parse(llm.generate([prompt.format(input="how can langsmith help with testing?")])))