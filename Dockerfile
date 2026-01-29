FROM python:2.7

WORKDIR /app

RUN pip install coverage paho-mqtt==1.6.1

COPY . .

CMD ["python", "-m", "unittest", "discover", "tests", "-v"]
