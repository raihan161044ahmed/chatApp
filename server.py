from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import openai

openai.api_key = ''


class ChatRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = json.loads(post_data.decode('utf-8'))
        user_message = params.get('user_message', '')

        if user_message:
            chat_history = user_message

            # Call the chat_completion function to get assistant's reply
            assistant_reply = self.chat_completion(chat_history)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(
                {'assistant_reply': assistant_reply}).encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(
                {'error': 'Invalid request'}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('index.html', 'rb') as file:
            self.wfile.write(file.read())

    def chat_completion(self, prompt):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ]
        )
        return response.choices[0].message.content


def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ChatRequestHandler)
    print('Starting chat server on http://localhost:8000...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
