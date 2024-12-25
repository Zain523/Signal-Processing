from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from Signal_processing import reduce_noise


app = Flask("my-app")
CORS(app)

@app.route('/', methods=['OPTIONS', 'POST'])
def index():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'https://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    if request.method == 'POST':
        data = request.get_json()
        file_path = data.get("audio_file")
        technique = data.get("technique")
        try:
            filter_audio_path = reduce_noise(file_path, technique)
            return {'response': filter_audio_path}
        except Exception as e:
            return jsonify({'response': "Something went wrong", 'error': e}), 500

if __name__ == '__main__':
    app.run(debug=True)
