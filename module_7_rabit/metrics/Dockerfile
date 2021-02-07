FROM python:3.8

WORKDIR /usr/src/app
RUN mkdir /logs
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./metric.py .
CMD ["/bin/bash", "-c", "python ./metric.py"]
# > /logs/labels_log.txt"]