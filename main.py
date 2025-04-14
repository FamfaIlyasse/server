from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

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

                        // Envoi des données au serveur (simulation)
                        fetch("/log", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify(data)
                        }}).then(() => {{
                            // Rediriger vers un faux PDF après envoi
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

        elif self.path == "/log":
            self.send_response(200)
            self.end_headers()
            print("[+] Données reçues :")

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
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            print("\n[+] Données reçues :")
            print(post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Donnees recues")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    PORT = int(os.environ.get("PORT", 8080))
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, CVEHandler)
    print(f"Serveur démarré sur http://0.0.0.0:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
