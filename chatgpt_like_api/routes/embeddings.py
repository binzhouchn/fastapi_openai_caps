#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse
from utils import torch_gc
import numpy as np
from loguru import logger
from datamodels import EmbeddingsBody

embedding_model = os.getenv('EMBEDDING_MODEL')
if embedding_model:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer(embedding_model)
else:
    class RandomSentenceTransformer:
        def encode(self, texts):
            logger.error("请配置 EMBEDDING_MODEL")
            return np.random.random((len(texts), 64))
    embedding_model = RandomSentenceTransformer()

router = APIRouter()

def do_embeddings(body: EmbeddingsBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)

    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    if not embedding_model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Embeddings model not found!")

    texts = body.input
    if isinstance(texts, str):
        texts = [texts]

    embeddings = embedding_model.encode(texts)

    data = []
    for i, embed in enumerate(embeddings):
        data.append({
            "object": "embedding",
            "index": i,
            "embedding": embed.tolist(),
        })
    content = {
        "object": "list",
        "data": data,
        "model": "text-embedding-ada-002-v2",
        "usage": {
            "prompt_tokens": 0,
            "total_tokens": 0
        }
    }
    return JSONResponse(status_code=200, content=content)


@router.post("/v1/embeddings")
async def embeddings(body: EmbeddingsBody, request: Request, background_tasks: BackgroundTasks):
    return do_embeddings(body, request, background_tasks)


@router.post("/v1/engines/{engine}/embeddings")
async def engines_embeddings(engine: str, body: EmbeddingsBody, request: Request, background_tasks: BackgroundTasks):
    return do_embeddings(body, request, background_tasks)
