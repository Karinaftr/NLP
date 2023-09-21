FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y libsndfile1-dev
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
