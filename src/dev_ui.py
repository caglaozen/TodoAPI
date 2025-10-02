#!/usr/bin/env python3
"""
ADK Dev UI starter script
"""
import os
import sys

sys.path.append("/app/src")


def main():
    """Start the ADK development UI"""
    try:
        print("Initializing ADK Dev UI...")

        # Import after path setup
        from google.adk.runners import DevUIRunner

        from agent.agent_service import TodoAgentService

        # Initialize the agent service
        agent_service = TodoAgentService()
        agent = agent_service.get_agent()

        # Start the development UI
        print("Starting ADK Dev UI...")
        print("Available at: http://localhost:8001/dev-ui/?app=todo_assistant")

        runner = DevUIRunner(agents=[agent], port=8001, host="0.0.0.0")
        runner.run()

    except ImportError as e:
        print(f"Import error: {e}")
        print("ADK Dev UI module not available. Starting basic web server...")
        start_basic_server()

    except Exception as e:
        print(f"Error starting dev UI: {e}")
        print("Starting basic web server...")
        start_basic_server()


def start_basic_server():
    """Start a basic HTTP server for testing"""
    import http.server
    import socketserver

    PORT = 8001

    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/dev-ui/" or self.path.startswith("/dev-ui/"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = """
                <html>
                <head><title>ADK Dev UI - TODO Assistant</title></head>
                <body>
                    <h1>ADK Dev UI - TODO Assistant</h1>
                    <p>This is a basic version of the ADK Development UI.</p>
                    <p>To test the agent, use the main API:</p>
                    <pre>
curl -X POST http://localhost:8000/agent/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hello!"}'
                    </pre>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
            else:
                super().do_GET()

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
