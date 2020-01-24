FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app

WORKDIR /app
COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

COPY app/ /app/

CMD /app/run
