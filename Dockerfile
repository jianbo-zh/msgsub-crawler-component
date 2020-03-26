FROM python:3.8.2-alpine3.11-me

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

CMD ["python", "./run.py"]