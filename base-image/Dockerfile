FROM debian:11

# Update package lists and install required dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip

# Add the Coral Edge TPU package repository
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list

RUN apt-get update

# Install the Edge TPU compiler
RUN apt-get install -y edgetpu-compiler

# Install Python dependencies
RUN pip3 install Flask pillow
