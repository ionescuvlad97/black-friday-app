FROM python:3.8-slim-buster
ENV STATIC_URL /static
ENV STATIC_PATH /usr/src/app/static
WORKDIR /usr/src/app
ADD . ./usr/src/app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r ./usr/src/app/requirements.txt
