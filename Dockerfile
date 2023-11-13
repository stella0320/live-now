FROM python:3.10.12-slim
 
WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ADD . /app

CMD python3 app.py