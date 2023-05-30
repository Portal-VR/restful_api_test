FROM python:3.10

WORKDIR /main_api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python3", "main.py"]
