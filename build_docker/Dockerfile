FROM python:3.10.13

#设置环境变量
ENV TZ Asia/Shanghai
ENV LANG zh_CN.UTF-8

# 安装基础包
RUN apt-get update && \
    apt-get install -y wget vim openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 解决vim中文乱码
RUN echo 'set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936 \n\
set termencoding=utf-8 \n\
set encoding=utf-8' >> ~/.vimrc

# Install python packages
RUN python -m pip install --upgrade pip \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi==0.115.4 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pydantic==2.9.2 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple scikit-learn==1.4.2 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jieba==0.42.1 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple starlette==0.41.2 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sse_starlette==1.8.2 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas==2.0.3 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple meutils==2024.09.19.17.11.07 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy==1.24.4 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple loguru==0.7.2 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple json==2.0.9 \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple openai==1.54.3

# 设置工作目录
WORKDIR /workspace

