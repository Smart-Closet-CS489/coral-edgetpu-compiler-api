FROM debian:11

RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
    
RUN apt-get update
    
RUN apt-get install edgetpu-compiler

RUN pip3 install Flask pillow

WORKDIR /app

COPY . /app

EXPOSE 80

CMD ["python3", "api.py"]
