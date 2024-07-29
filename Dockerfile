FROM python:3.12-alpine
LABEL authors="amedix"
WORKDIR /app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "-u", "dota_patch.py"]