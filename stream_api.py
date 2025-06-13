from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream_data():
    # Generate or return a stream of integers (for demo)
    stream = [random.randint(1, 100) for _ in range(10)]
    return jsonify({'data': stream})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
