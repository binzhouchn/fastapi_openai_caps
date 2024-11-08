#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional, List, Any

class Message(BaseModel):
    role: str
    content: str


class ChatBody(BaseModel):
    user: str = None
    model: str
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 100000
    temperature: Optional[float] = 0.1
    top_p: Optional[float] = 0.9

    messages: List[Message]  # Chat

    # 本地大模型
    knowledge_base: str = None


class CompletionBody(BaseModel):
    user: str = None
    model: str
    stream: Optional[bool] = False
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]

    prompt: str  # Prompt

    # 本地大模型
    knowledge_base: str = None


class EmbeddingsBody(BaseModel):
    # Python 3.8 does not support str | List[str]
    input: Any
    model: Optional[str]