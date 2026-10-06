import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LITHOSAI_API_KEY"],
    base_url="https://api.lithosai.cloud/v1",
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4.1-Flash",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
