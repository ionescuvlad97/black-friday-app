FROM python:3.8-slim-buster
WORKDIR /usr/src/app
ADD . ./usr/src/app
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r ./usr/src/app/requirements.txt
# VOLUME ./scraper ./usr/src/app
# CMD [ "python", "./usr/src/app/scripts/create_database.py" ]
