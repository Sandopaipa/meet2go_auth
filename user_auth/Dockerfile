FROM python:latest
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /meet2go_auth
COPY requirements.txt /meet2go_auth/requirements.txt
RUN pip install -r requirements.txt
COPY . /meet2go_auth