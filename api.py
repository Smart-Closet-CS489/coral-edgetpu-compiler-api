import os
import sys
import zipfile
from flask import Flask, request, jsonify, send_file
import subprocess

app = Flask(__name__)

# Define an endpoint to accept multiple .tflite files and compile them
@app.route('/compile', methods=['POST'])
def compile_models():
    # Check if 'models' is part of the request (multiple files can be uploaded under 'models')
    if 'models' not in request.files:
        return jsonify({"error": "No model files provided"}), 400
    
    models = request.files.getlist('models')  # Get the list of files with the key 'models'
    
    if not models:
        return jsonify({"error": "No models provided"}), 400
    
    # Ensure the models directory exists
    os.makedirs('/app/models', exist_ok=True)
    compiled_models = []
    log_file_path = "/app/model_compile_log.txt"

    # Open the log file to write output
    with open(log_file_path, 'a') as log_file:
        for model_file in models:
            model_path = f'/app/models/{model_file.filename}'  # Define path for each model file

            # Save the uploaded model to the specified file path
            model_file.save(model_path)
            
            # Log file path
            log_file.write(f"Size of uploaded model {model_file.filename}: {os.path.getsize(model_path)} bytes\n")

        COMPILER_PATH = "/usr/bin/edgetpu_compiler"  # Path to compiler

        # Prepare a list of model paths to compile
        model_paths = [f'/app/models/{model.filename}' for model in models]

        # Run the Edge TPU compiler for all models in the list
        try:
            # Run the compiler for the list of models (co-compilation)
            result = subprocess.run([COMPILER_PATH] + model_paths, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Log stdout and stderr to the log file
            log_file.write(f"Compiler stdout: {result.stdout.decode()}\n")
            log_file.write(f"Compiler stderr: {result.stderr.decode()}\n")

            # Find the compiled model(s) dynamically by searching for files with _edgetpu.tflite
            for file in os.listdir('.'):
                if file.endswith('_edgetpu.tflite'):
                    compiled_model_path = os.path.join('.', file)
                    compiled_models.append(compiled_model_path)
                    log_file.write(f"Compiled model saved at: {compiled_model_path}\n")
                    log_file.write(f"Size of compiled model: {os.path.getsize(compiled_model_path)} bytes\n")

        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Error compiling models: {e.stderr.decode()}"}), 500

    # After processing all models, return a ZIP file containing the compiled models
    if compiled_models:
        # Create a ZIP file
        zip_filename = "/app/compiled_models.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for compiled_model in compiled_models:
                zipf.write(compiled_model, os.path.basename(compiled_model))

        # Send the ZIP file as a response
        return send_file(zip_filename, as_attachment=True, download_name="compiled_models.zip")

    else:
        return jsonify({"error": "No models were compiled successfully"}), 500

    finally:
        # Clean up the original model files
        for model_file in models:
            model_path = f'/app/models/{model_file.filename}'
            if os.path.exists(model_path):
                os.remove(model_path)
        # Clean up the compiled models
        for compiled_model in compiled_models:
            if os.path.exists(compiled_model):
                os.remove(compiled_model)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
