FROM python:3.8-slim
RUN apt-get update && apt-get install -y iputils-ping
RUN pip install argparse rich_argparse

WORKDIR script
COPY script.py .

ENTRYPOINT ["python3", "script.py"]
