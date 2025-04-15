from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys
import socket

class CVEHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip("/")

        if path.startswith("cve-"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>CVE Report - {path.upper()}</title>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
                <style>
                    body {{
                        font-family: 'Inter', sans-serif;
                        background-color: #0f0f0f;
                        color: #f5f5f5;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        margin: 0;
                    }}
                    h1 {{
                        font-size: 2.5rem;
                        margin-bottom: 1rem;
                    }}
                    p {{
                        font-size: 1.2rem;
                        margin-bottom: 2rem;
                    }}
                    button {{
                        background-color: #007bff;
                        color: white;
                        padding: 0.8rem 1.5rem;
                        border: none;
                        border-radius: 8px;
                        font-size: 1rem;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }}
                    button:hover {{
                        background-color: #0056b3;
                    }}
                </style>
                <script>
                    function collectAndDownload() {{
                        const data = {{
                            userAgent: navigator.userAgent,
                            referrer: document.referrer,
                            time: new Date().toISOString()
                        }};

                        fetch("/log", {{
                            method: "POST",
                            headers: {{
                                "Content-Type": "application/json"
                            }},
                            body: JSON.stringify(data)
                        }}).then(() => {{
                            window.location.href = "/downloads/security-report.pdf";
                        }});
                    }}
                </script>
            </head>
            <body>
                <h1>Détails pour {path.upper()}</h1>
                <p>Un rapport critique a été généré. Cliquez pour le télécharger :</p>
                <button onclick="collectAndDownload()">📄 Télécharger le rapport</button>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))

        elif self.path == "/downloads/security-report.pdf":
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", "attachment; filename=security-report.pdf")
            self.end_headers()
            self.wfile.write(b"%PDF-1.5 fake-pdf-content-for-simulation")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page non trouvee")

    def do_POST(self):
        if self.path == "/log":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            client_ip = self.client_address[0]

            print("\n[+] Donnees recues (POST /log) :")
            print(f"IP: {client_ip}")
            print(post_data, flush=True)

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Donnees recues")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, CVEHandler)
    print(f"Serveur en ligne sur http://0.0.0.0:{port}", flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
