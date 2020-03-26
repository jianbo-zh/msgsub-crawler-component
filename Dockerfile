FROM python:3.8.2-alpine3.11-gcc
ENV PATH /usr/local/bin:$PATH

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ADD . /code
WORKDIR /code
CMD ./run.py