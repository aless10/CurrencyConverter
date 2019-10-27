FROM alpine:latest

# workaround to install pylint>=2.0.0
RUN apk add --no-cache --update python3-dev py-pip gcc build-base libxslt-dev --update bash vim

COPY ./convert_app /app/convert_app
COPY ./requirements.txt /app/requirements.txt
COPY ./.bumpversion.cfg /app/.bumpversion.cfg

WORKDIR /app

RUN export PATH=/app:${PATH}
RUN mkdir logs && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt

RUN env

CMD ["python3", "convert_app/wsgi.py"]
