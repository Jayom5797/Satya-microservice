"""
Simple HTTP server to serve the frontend
"""

import http.server
import socketserver
import os

PORT = 3001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("🌐 Frontend Server Starting")
        print("=" * 60)
        print(f"📡 Server running at: http://localhost:{PORT}")
        print(f"📁 Serving directory: {DIRECTORY}")
        print("=" * 60)
        print("\n✨ Open http://localhost:3000 in your browser")
        print("Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
