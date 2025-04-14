from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

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
                <title>CVE Details</title>
                <script>
                    function collectAndDownload() {{
                        const data = {{
                            ip: "127.0.0.1",
                            userAgent: navigator.userAgent,
                            referrer: document.referrer,
                            time: new Date().toISOString()
                        }};

                        fetch("/log", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify(data)
                        }}).then(() => {{
                            window.location.href = "/downloads/security-report.pdf";
                        }});
                    }}
                </script>
            </head>
            <body>
                <h1>Détails pour {path.upper()}</h1>
                <p>Téléchargez le rapport de sécurité critique :</p>
                <button onclick="collectAndDownload()">Télécharger le rapport</button>
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
            post_data = self.rfile.read(content_length)

            # Affiche les données dans les logs Render
            print("\n[+] Données reçues (POST /log) :")
            print(post_data.decode("utf-8"), flush=True)

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Données reçues")
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
