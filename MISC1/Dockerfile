FROM python:3.9-slim
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY app/* /
EXPOSE 8088
COPY main.py main.py
ENTRYPOINT ["python", "main.py"]