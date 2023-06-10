FROM python:3.10.10-bullseye

# Install dependencies
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "run.py"]

# CMD [ "gunicorn", "run:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:3000" ]


