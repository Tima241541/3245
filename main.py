import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from bot import main as start_bot

# Минимальный веб-сервер, чтобы Render не закрывал сервис
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Запускаем фейковый веб-сервер в отдельном потоке
    threading.Thread(target=run_web_server, daemon=True).start()
    # Запускаем бота
    asyncio.run(start_bot())