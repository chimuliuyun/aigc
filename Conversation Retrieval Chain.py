from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever

# 创建Ollama模型实例
llm = Ollama(model="llama2")
print("Ollama模型加载完成")

# 创建WebBaseLoader加载器实例
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
print("WebBaseLoader实例创建完成")

# 加载文档
docs = loader.load()
print(f"文档加载完成，共{len(docs)}篇文档")

# 初始化OllamaEmbeddings和文本拆分器
embeddings = OllamaEmbeddings()
text_splitter = RecursiveCharacterTextSplitter()

# 拆分文档
documents = text_splitter.split_documents(docs)
print(f"文档拆分完成，拆分后共{len(documents)}个文档")

# 使用FAISS创建向量存储
vector = FAISS.from_documents(documents, embeddings)
print("FAISS向量存储创建完成")

# 创建文档链
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)
print("文档链创建完成")

# 创建检索器链
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
print("检索器链创建完成")

# 创建带有历史记录意识的检索器链
prompt_history_aware = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt_history_aware)
print("带有历史记录意识的检索器链创建完成")

# 模拟对话历史
chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
print("模拟对话历史创建完成")

# 调用带有历史记录意识的检索器链
retriever_chain_output = retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})
print("带有历史记录意识的检索器链调用完成")

# 创建文档链
prompt_document_chain = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, prompt_document_chain)
print("文档链创建完成")

# 创建检索器链
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
print("检索器链创建完成")

# 再次模拟对话历史
chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
print("再次模拟对话历史创建完成")

# 调用检索器链
retrieval_chain_output = retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})
print("检索器链调用完成")
print("最终输出:", retrieval_chain_output)
