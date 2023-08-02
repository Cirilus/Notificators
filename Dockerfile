FROM python:alpine

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1


RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./ ./

RUN crontab /app/crontab
RUN touch /tmp/out.log

CMD crond && tail -f /tmp/out.log