# openai api接口标准格式封装

## 1.环境部署

方式一：可以直接安装python环境和requirements.txt文件中的所有包<br>

方式二：根据我提供的Dockerfile构建docker<br>

```shell
cd build_docker
docker build -t fastapi_openai_py310:v1 .
```

## 2.修改部分代码

以api调用为例，修改chatgpt_like_api/routes/completions.py文件中13至20行

## 3.运行

建议用docker来运行，运行脚本我已经写好，<br>

```shell
sudo sh run.sh
```

## 4.调用示例

4.1 curl调用示例<br>

```shell
curl http://localhost:8899/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xmatrix" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "您是一个人工智能助手。您的首要任务是帮助用户实现他们的请求，以实现用户的满足感。"
      },
      {
        "role": "user",
        "content": "鲁迅和周树人是什么关系"
      }
    ],
    "use_search": false,
    "stream": false
  }'
```

4.2 python调用示例<br>

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url = "http://localhost:8899/v1",
    api_key="sk-xmatrix",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "鲁迅和周树人是什么关系",
        }
    ],
    stream=False,
    model="gpt-3.5-turbo"
)

print(chat_completion)
'''
ChatCompletion(id='chatcmpl-1561bf24-9d94-11ef-8c81-86ee95f98041', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='鲁迅和周树人其实是同一个人。鲁迅是周树人的笔名。以下是一些详细信息：\n\n- **周树人**：这是鲁迅的本名，出生于1881年9月25日。\n- **鲁迅**：这是他的最著称的笔名，他以此名发表了大量的文学作品，包括小说、杂文、散文和翻译作品等。\n\n鲁迅是中国现代文学的重要作家、思想家，也是新文化运动的重要参与者之一。他的作品如《狂人日记》、《阿Q正传》等，对中国社会进行了深刻的批判和反思。\n\n所以，鲁迅和周树人是同一个人的两个名字。', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))], created=1731044484, model='gpt-3.5-turbo', object='chat.completion', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0, completion_tokens_details=None, prompt_tokens_details=None), user=None)
'''
```
