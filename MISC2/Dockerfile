FROM python:3.7-slim
WORKDIR /
COPY app/* /
RUN pip install --upgrade pip setuptools
RUN apt-get update && apt-get install zip vim inetutils-ping -y
RUN pip install -r /requirements.txt
COPY main.py main.py
COPY run.sh /
RUN chmod 777 /run.sh
ENTRYPOINT ["/run.sh"]
EXPOSE 8080
