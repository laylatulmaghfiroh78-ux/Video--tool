import http.server
import socketserver
import urllib.parse
import html

PORT = 8000


def buat_prompt(produk, gerakan, durasi, gaya):
    produk = html.escape(produk)
    gerakan = html.escape(gerakan)
    durasi = html.escape(durasi)
    gaya = html.escape(gaya)

    return f"""VIDEO PROMPT — FERA FASHION

Durasi: {durasi} detik
Gaya: {gaya}

Tampilkan produk fashion berikut:
{produk}

Gerakan model:
{gerakan}

Instruksi:
- Pertahankan model pakaian, warna, motif, bahan, jahitan dan detail produk persis seperti produk asli.
- Jangan mengubah desain pakaian.
- Gerakan model natural dan elegan seperti model profesional.
- Pergerakan kamera halus dan realistis.
- Pencahayaan natural dan konsisten.
- Tekstur kain terlihat jelas dan tajam.
- Hasil video realistis seperti direkam menggunakan kamera digital/flagship.
- Tidak ada perubahan bentuk tubuh yang tidak wajar.
- Tidak ada objek tambahan yang tidak diperlukan.
- Tidak ada efek CGI atau tampilan seperti AI.
- Komposisi vertikal 9:16.
- Cocok untuk konten promosi TikTok/Reels.

HASIL AKHIR:
Video fashion realistis, natural, tajam, profesional dan fokus pada produk."""
    

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Video Tool - Fera Fashion</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    margin: 0;
    padding: 20px;
}
.container {
    max-width: 700px;
    margin: auto;
    background: white;
    padding: 25px;
    border-radius: 18px;
}
h1 {
    text-align: center;
}
label {
    display: block;
    margin-top: 15px;
    font-weight: bold;
}
input, textarea, select {
    width: 100%;
    box-sizing: border-box;
    padding: 12px;
    margin-top: 7px;
    border: 1px solid #ccc;
    border-radius: 10px;
    font-size: 15px;
}
textarea {
    min-height: 110px;
}
button {
    width: 100%;
    padding: 14px;
    margin-top: 20px;
    border: 0;
    border-radius: 10px;
    background: #168a3b;
    color: white;
    font-size: 17px;
    font-weight: bold;
}
.result {
    margin-top: 25px;
}
pre {
    white-space: pre-wrap;
    background: #f1f1f1;
    padding: 15px;
    border-radius: 10px;
}
</style>
</head>

<body>
<div class="container">

<h1>🎬 Video Tool</h1>
<p style="text-align:center;">Pembuat Prompt Video Fera Fashion</p>

<form method="POST">

<label>Produk</label>
<textarea name="produk" placeholder="Contoh: Gamis wanita bahan combat warna biru, model elegan..."></textarea>

<label>Gerakan Model</label>
<textarea name="gerakan" placeholder="Contoh: Model berjalan perlahan, kemudian berputar untuk memperlihatkan detail gamis..."></textarea>

<label>Durasi</label>
<select name="durasi">
<option>10 detik</option>
<option>14 detik</option>
<option>15 detik</option>
<option>20 detik</option>
</select>

<label>Gaya Video</label>
<select name="gaya">
<option>ASMR natural realistis</option>
<option>Natural realistis</option>
<option>Fashion profesional</option>
<option>Promosi TikTok</option>
</select>

<button type="submit">✨ BUAT PROMPT</button>

</form>
"""

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        halaman = HTML + "</div></body></html>"
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(halaman.encode("utf-8"))

    def do_POST(self):
        panjang = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(panjang).decode("utf-8")
        form = urllib.parse.parse_qs(data)

        produk = form.get("produk", [""])[0]
        gerakan = form.get("gerakan", [""])[0]
        durasi = form.get("durasi", ["10 detik"])[0]
        gaya = form.get("gaya", ["ASMR natural realistis"])[0]

        prompt = buat_prompt(produk, gerakan, durasi, gaya)

        halaman = HTML + f"""
<div class="result">
<h2>✅ Prompt Kamu</h2>
<pre>{prompt}</pre>
</div>
</div>
</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(halaman.encode("utf-8"))


with socketserver.TCPServer(("", PORT), Handler) as server:
    print(f"Video Tool berjalan di port {PORT}")
    server.serve_forever()
