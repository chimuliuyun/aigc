from volcenginesdkarkruntime import Ark
import os
from Langsmith import langsmith

# 设置环境变量
os.environ["ARK_API_KEY"] = "doubao_api_key"

# 创建 Langsmith 实例
langsmith = langsmith.Langsmith()

# 创建 Ark 客户端
client = Ark(api_key="doubao_api_key")

# 非流式请求
print("----- standard request -----")
langsmith.track("Sending standard chat completion request")

# 创建聊天补全请求
completion = client.chat.completions.create(
    model="ep-20240804223930-krfgb",
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)

# 记录事件
langsmith.track("Received completion result for standard request")

# 打印补全结果
print(completion.choices[0].message.content)

# 流式请求
print("----- streaming request -----")
langsmith.track("Sending streaming chat completion request")

# 创建流式聊天补全请求
stream = client.chat.completions.create(
    model="ep-20240804223930-krfgb",
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    stream=True
)

# 记录事件
langsmith.track("Started streaming completion results")

# 遍历流式补全结果
for chunk in stream:
    if chunk.choices:
        # 打印补全结果
        print(chunk.choices[0].delta.content, end="")

# 记录事件
langsmith.track("Finished streaming completion results")

print()

# 记录流程结束
langsmith.track("Completed the process")

# 将记录保存到文件中
langsmith.save("langsmith_project_record.json")
