FROM python:3.13.12

COPY . /JedhaProject/

CMD python /JedhaProject/main.py

ENTRYPOINT python /JedhaProject/main.py