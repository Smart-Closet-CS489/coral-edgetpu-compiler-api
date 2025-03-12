# coral-edgetpu-compiler-api

Simple flask api for accepting .tflite files, and compiling them to a version of tflite compatible with the edge tpu runtime (specifically for running on the google coral USB).

We need this becasue the compiler does not exist for ARM64, therefore, we need a simple x86 server to handle the compilation step.


# steps

1. cd into coral-edgetpu-compiler-api/

2. run the following command to build the docker container:

docker build -t coral-edgetpu-compiler-api .

3. run the following command to run the container and start the api

docker run -p 80:80 --rm coral-edgetpu-compiler-api

4. to compile a .tflite file, send a request to 134.199.176.64:80/compile and put the .tflite file in the body of the POST request