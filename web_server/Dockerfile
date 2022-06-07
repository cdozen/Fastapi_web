FROM python:3.9

RUN apt-get update && apt-get -y upgrade

WORKDIR /code

# install dependencies

COPY requirements ./requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/docker.txt

# install this package

COPY web_server ./web_server
COPY setup.py ./
RUN pip install -e .

# create user

RUN useradd --create-home appuser
USER appuser

#CMD ["uvicorn", "web_server.app_test:app", "--host", "0.0.0.0", "--port", "80"]
