from volcenginesdkarkruntime import Ark
import os
# 设置环境变量
os.environ["ARK_API_KEY"] = "doubao_api_key"
# 创建客户端
client = Ark(
    api_key="doubao_api_key",
)

# Non-streaming:
print("----- standard request -----")
# 创建聊天补全请求
completion = client.chat.completions.create(
    model="ep-20240804223930-krfgb",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
# 打印补全结果
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
# 创建流式聊天补全请求
stream = client.chat.completions.create(
    model="ep-20240804223930-krfgb",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    stream=True
)
# 遍历流式补全结果
for chunk in stream:
    # 如果没有补全结果，则跳过
    if not chunk.choices:
        continue
    # 打印补全结果
    print(chunk.choices[0].delta.content, end="")
print()