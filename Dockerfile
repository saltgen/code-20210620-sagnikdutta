FROM python:3.6-alpine

# dockerize being installed below 
# will be required for unittests later

RUN apk add --no-cache openssl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz


# Creating a user for installing pip packages for the same
# This is not necessary but is a good practice

RUN adduser -D worker
USER worker
WORKDIR /home/worker

COPY --chown=worker:worker requirements.txt requirements.txt
ENV PATH="/home/worker/.local/bin:${PATH}"

RUN pip install --upgrade pip setuptools wheel
RUN pip install --user -r requirements.txt

COPY --chown=worker:worker . .

# Copying project code

WORKDIR /app
ADD src /app/src
ADD tests /app/tests
COPY gunicorn.conf.py /app

LABEL maintainer="Sagnik Dutta <sdnirvana94@gmail.com>" version="1.0.0"

# Launching api app

CMD /home/worker/.local/bin/gunicorn "src.main:create_app()"