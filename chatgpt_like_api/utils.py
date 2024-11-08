#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from meutils.pipe import *
from meutils.db import MySQL
from meutils.decorators import clear_cuda_cache

#####################load_llm4chat开始#####################
# MODEL_BASE = {'chatglm'}
def load_llm4chat(model_name_or_path="THUDM/chatglm-6b", device='cpu', num_gpus=2, model_base=None, **kwargs):
    if not model_base:  # 模型基座
        model_base = Path(model_name_or_path).name.lower()
        for p in Path(__file__).parent.glob('*.py'):
            if p.stem in model_base:
                # logger.warning(p) # 自动推断模型基座
                model_base = p.stem

    logger.info(f"MODEL_BASE: {model_base}")  # 打印模型基座

    try:
        model_base = importlib.import_module(f"chatllm.llms.{model_base}")
        do_chat = model_base.load_llm4chat(
            model_name_or_path=model_name_or_path,
            device=device,
            num_gpus=num_gpus,
            **kwargs)
        return do_chat

    except Exception as e:
        logger.info(f"using api instead of local model.")

        def do_chat(query, **kwargs):  # DEV
            for i in f"🔥🔥🔥\n\n生产环境请配置 LLM_MODEL ⚠️\n\n🔥🔥🔥\n":
                time.sleep(0.2)
                yield i

        return do_chat
#####################load_llm4chat加载结束#####################

torch_gc = clear_cuda_cache(lambda: logger.info('Clear GPU'), bins=os.getenv('TIME_INTERVAL', 15))

###############配置###############
debug = os.getenv('DEBUG')

tokens = set(os.getenv('TOKENS', 'sk-xmatrix').split(',')) #可自行修改
llm_model = os.getenv('LLM_MODEL', '')
embedding_model = os.getenv('EMBEDDING_MODEL')
device = os.getenv('DEVICE', 'cpu')
num_gpus = int(os.getenv('NUM_GPUS', 2))

llm_role = os.getenv('LLM_ROLE', '')

# 落库
db_url = os.getenv('DB_URL', '')
table_name = os.getenv('TABLE_NAME', 'llm')
###################################


if embedding_model:
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer(embedding_model)
else:
    class RandomSentenceTransformer:
        def encode(self, texts):
            logger.error("请配置 EMBEDDING_MODEL")
            return np.random.random((len(texts), 64))


    embedding_model = RandomSentenceTransformer()

# 获取 do_chat
_do_chat = load_llm4chat(model_name_or_path=llm_model, device=device, num_gpus=num_gpus)


def do_chat(query, **kwargs):
    if llm_role:
        query = """{role}\n请回答以下问题\n{question}""".format(question=query, role=llm_role)  # 增加角色扮演
    return _do_chat(query, **kwargs)


# 入库
def do_db(df: pd.DataFrame, table_name: str):
    try:
        import emoji
        df = df.astype(str)
        df['choices'] = df['choices'].astype(str).map(emoji.demojize)  # todo: 更优雅的解决方案
        if db_url:
            db = MySQL(db_url)
            db.create_table_or_upsert(df, table_name)
            if debug:
                logger.debug("Data written successfully 👍")
    except Exception as e:
        logger.error(f"Failed to write data ⚠️: {e}")
