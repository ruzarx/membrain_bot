FROM python:3.11
USER root

RUN mkdir -p /code
WORKDIR /code

RUN apt-get update

COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD ["app.py"]
