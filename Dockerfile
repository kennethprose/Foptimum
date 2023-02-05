FROM python:3.10-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

RUN apk update
RUN apk add iputils

ADD speedtest.py .
ADD speedtest .

EXPOSE 9191

CMD [ "python", "./speedtest.py" ]