docker run -v $PWD/chatgpt_like_api:/workspace/chatgpt_like_api -w /workspace/chatgpt_like_api -p 8899:8899 -d fastapi_openai_py310:v1 python app.py
