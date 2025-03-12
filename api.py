import os
import sys
from flask import Flask, request, jsonify, send_file
import subprocess

app = Flask(__name__)

# Define an endpoint to accept a .tflite file and compile it
@app.route('/compile', methods=['POST'])
def compile_model():
    if 'model' not in request.files:
        return jsonify({"error": "No model file provided"}), 400
    
    model_file = request.files['model']
    
    # Define a path for the original model file
    model_path = '/app/models/input_model.tflite'  # Path for saving the uploaded model
    # Ensure the directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the uploaded model to the specified file path
    model_file.save(model_path)
    
    # Log file path
    log_file_path = "/app/model_compile_log.txt"

    # Open the log file to write output
    with open(log_file_path, 'a') as log_file:
        # Write the size of the uploaded model to the log file
        log_file.write(f"Size of uploaded model: {os.path.getsize(model_path)} bytes\n")

    COMPILER_PATH = "/usr/bin/edgetpu_compiler"  # Adjust to where the compiler is installed

    # Run the Edge TPU compiler
    try:
        # Run the compiler and specify the output directory (default is the current directory)
        result = subprocess.run([COMPILER_PATH, model_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Log stdout and stderr to a file
        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Compiler stdout: {result.stdout.decode()}\n")
            log_file.write(f"Compiler stderr: {result.stderr.decode()}\n")
        
        # Find the compiled model file dynamically by searching for files with .tflite
        compiled_model_path = None
        for file in os.listdir('.'):
            if file.endswith('_edgetpu.tflite'):
                compiled_model_path = os.path.join('.', file)
                break

        # Check if we found the compiled model
        if compiled_model_path and os.path.exists(compiled_model_path):
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Compiled model saved at: {compiled_model_path}\n")
                log_file.write(f"Size of compiled model: {os.path.getsize(compiled_model_path)} bytes\n")
            
            # Send the compiled model as a response
            return send_file(compiled_model_path, as_attachment=True, download_name="compiled_model.tflite")
        else:
            return jsonify({"error": "Compiled model not found"}), 500

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error compiling model: {e.stderr.decode()}"}), 500

    finally:
        # Clean up the original and compiled model files
        if os.path.exists(model_path):
            os.remove(model_path)
        if compiled_model_path and os.path.exists(compiled_model_path):
            os.remove(compiled_model_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
