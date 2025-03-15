FROM coral-edgetpu-compiler-api-base-image
WORKDIR /app
COPY . /app
EXPOSE 8000
CMD ["python3", "api.py"]
