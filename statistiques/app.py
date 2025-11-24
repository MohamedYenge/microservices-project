
from flask import Flask, request, jsonify
import statistics

app = Flask(__name__)

@app.route('/mean', methods=['POST'])
def mean():
    data = request.get_json()
    nums = data['numbers']
    result = statistics.mean(nums)
    return jsonify({'mean': result})

@app.route('/median', methods=['POST'])
def median():
    data = request.get_json()
    nums = data['numbers']
    result = statistics.median(nums)
    return jsonify({'median': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
