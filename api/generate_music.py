import requests
import json
from http.server import BaseHTTPRequestHandler

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data)

        # Generate music
        audio_bytes = query({
            "inputs": payload.get("prompt", "classic calm and lofi music for podcast"),
        })

        # Return the audio file
        self.send_response(200)
        self.send_header('Content-type', 'audio/wav')
        self.end_headers()
        self.wfile.write(audio_bytes)

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'audio/wav'},
        'body': query({"inputs": "classic calm and lofi music for podcast"}),
        'isBase64Encoded': True,
    }