from volcenginesdkarkruntime import Ark
import os
os.environ["ARK_API_KEY"] = "doubao_api_key"
client = Ark(
    api_key="doubao_api_key",
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="ep-20240804223930-krfgb",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    model="ep-20240804223930-krfgb",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    stream=True
)
for chunk in stream:
    if not chunk.choices:
        continue
    print(chunk.choices[0].delta.content, end="")
print()