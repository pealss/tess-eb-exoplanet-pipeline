FROM nvidia/cuda:11.8.0-base
RUN apt-get update && apt-get install -y python3.9 git
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["prefect", "orion", "start"]