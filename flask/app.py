from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def predict():
    query_data = request.get_json()
    query = query_data['query']

    prediction = query + '_predicted'

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0')