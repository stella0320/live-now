FROM python:3.10.12-slim
 
WORKDIR /app/live-now

ADD ./requirements.txt /app/live-now/requirements.txt

RUN pip install -r requirements.txt

ADD . /app/live-now

CMD python3 app.py