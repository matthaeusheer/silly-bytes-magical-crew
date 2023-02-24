import json
import logging
import azure.functions as func

from flask import Flask, request

# Initialize Flask app
app = Flask(__name__)

# Dictionary to store posted texts
texts = {}


@app.route('/api/texts', methods=['POST'])
def create_text():
    # Validate request payload
    if not request.json or 'text' not in request.json:
        return json.dumps({'error': 'Invalid payload'}), 400

    text = request.json['text']
    text_id = len(texts) + 1
    texts[text_id] = text

    return json.dumps({'id': text_id}), 201


@app.route('/api/texts/<int:text_id>', methods=['DELETE'])
def delete_text(text_id):
    # Check if text exists
    if text_id not in texts:
        return json.dumps({'error': 'Text not found'}), 404

    # Delete text
    del texts[text_id]

    return '', 204


@app.route('/api/texts', methods=['GET'])
def get_texts():
    return json.dumps(texts)


@app.route('/api/texts/search', methods=['GET'])
def search_text():
    # Validate query parameter
    if 'q' not in request.args:
        return json.dumps({'error': 'Query parameter "q" required'}), 400

    query = request.args['q']

    # Search for query in texts
    for text_id, text in texts.items():
        if query in text:
            return json.dumps({'id': text_id, 'text': text}), 200

    return json.dumps({'error': 'Text not found'}), 404


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    try:
        return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(status_code=500)

