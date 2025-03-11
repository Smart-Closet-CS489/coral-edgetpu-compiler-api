# coral-edgetpu-compiler-api

Simple flask api for accepting .tflite files, and compiling them to a version of tflite compatible with the edge tpu runtime (specifically for running on the google coral USB).

We need this becasue the compiler does not exist for ARM64, therefore, we need a simple x86 server to handle the compilation step.
