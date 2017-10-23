FROM alpine
RUN apk add --update --no-cache \
    python3 python3-dev \
    postgresql-dev \
    build-base ca-certificates

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN python3 -m pip install -r requirements.txt

COPY setup.py /app/
COPY sqlparser /app/sqlparser/

RUN python3 setup.py install

CMD ["sqlparser"]
