from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from Signal_processing import reduce_noise

app = Flask("my-app")
CORS(app)

@app.route('/', methods=['OPTIONS', 'POST'])
def index():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000/'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    if request.method == 'POST':
        # Check if the file is part of the request
        
        audio_file = request.files['file_path']
        technique = request.form.get("technique")
        
        try:
            file_path = f'Sample_audio/{audio_file.filename}'
            audio_file.save(file_path)

            # Process the file with the given technique
            filter_audio_path = reduce_noise(file_path, technique)

            # Return the path to the filtered audio file
            return jsonify({'response': filter_audio_path})

        except Exception as e:
            return jsonify({'response': 'Something went wrong', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


