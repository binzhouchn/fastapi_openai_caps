#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import Response, StreamingResponse, JSONResponse
from sse_starlette import EventSourceResponse
from rich import print as rprint
from meutils.pipe import *
from utils import *
from datamodels import *
from routes.responses import *
import json

####################### revise start #######################
from openai import OpenAI
client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key = os.getenv("XAI_API_KEY")
)
MODEL = "grok-beta"
####################### revise end #######################

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(body: ChatBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)
    _id = uuid.uuid1()

    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    # if not llm_model: # 空模型
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, "LLM model not found!")
    question = body.messages[-1]
    chat_kwargs = {"temperature": body.temperature, "top_p": body.top_p, "max_tokens": body.max_tokens}

    if question.role == 'user':
        question = question.content
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No Question Found")

    msgs_feed2chatgpt = []
    for message in body.messages:
        if message.role == 'system':
            msgs_feed2chatgpt.append({"role": "system", "content": message.content})
        if message.role == 'user':
            msgs_feed2chatgpt.append({"role": "user", "content": message.content})
        elif message.role == 'assistant':
            msgs_feed2chatgpt.append({"role": "assistant", "content": message.content})

    if debug:  # 日志
        rprint('Request:', json.loads(await request.body()))
        rprint('ChatBody:', body.dict())
    if body.stream:
        def eval_llm():
            first = True
            response = ''
            for _response in client.chat.completions.create(model=MODEL, messages=msgs_feed2chatgpt, stream=True):
                if _response.choices[0].delta.content:
                    response += _response.choices[0].delta.content
                    if first:
                        first = False
                        yield json.dumps(generate_stream_response_start(_id), ensure_ascii=False)
                    _ = generate_stream_response(_id, _response.choices[0].delta.content)
                    time.sleep(0.01)
                    yield json.dumps(_, ensure_ascii=False)
            yield json.dumps(generate_stream_response_stop(_id), ensure_ascii=False)
            yield "[DONE]"

            content = generate_response(_id, response)
            content['user'] = body.user
            rprint(content)
            background_tasks.add_task(do_db, pd.DataFrame([content]), 'chatcmpl')
            if debug: logger.success(content)  # 日志

        return EventSourceResponse(eval_llm(), ping=10000)
    else:
        response = ''.join([x.choices[0].delta.content for x in client.chat.completions.create(model=MODEL, messages=msgs_feed2chatgpt, stream=True) if x.choices[0].delta.content])

        content = generate_response(_id, response)
        content['user'] = body.user
        background_tasks.add_task(do_db, pd.DataFrame([content]), 'chatcmpl')

        if debug: logger.success(content)  # 日志

        return JSONResponse(content)

