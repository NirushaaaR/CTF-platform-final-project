FROM python:3.8-slim

# Not allow python to buffer output in docker (print directly)
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /src
WORKDIR /src
COPY ./src /src

# Don't run as root account!!
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser --disabled-password user
RUN chown -R user:user /vol/
RUN chmod -R 644 /vol/web
USER user 
# There seems to be an issue just run as root though