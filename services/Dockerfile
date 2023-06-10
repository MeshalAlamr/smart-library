FROM nvidia/cuda:11.7.0-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip poppler-utils tesseract-ocr\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python3 download_models.py

EXPOSE 8000

CMD ["python3", "app.py"]

# CMD [ "gunicorn", "app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000" ]

