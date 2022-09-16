FROM python:3.10-bullseye

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt update
RUN apt install inetutils-ping

ADD speedtest.py .
ADD speedtest .

EXPOSE 9191

CMD [ "python", "./speedtest.py" ]