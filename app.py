from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/get-link', methods=['POST'])
def get_link():
    data = request.get_json()
    url = data.get('url')
    req_type = data.get('type', 'mp4')
    
    if not url:
         return jsonify({"error": "Link nahi mila"})
         
    try:
        if req_type == 'thumb':
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return jsonify({"download_url": info.get('thumbnail')})

        # YAHAN CHANGE KIYA HAI: YouTube ki bot verification bypass karne ke liye options
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(id)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}}, # YouTube ko lagega app se request hai
        }

        if req_type == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            ydl_opts['merge_output_format'] = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = 'mp3' if req_type == 'mp3' else 'mp4'
            file_name = f"{info['id']}.{ext}"

            return jsonify({
                "download_url": f"/download-file/{file_name}"
            })
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)})

@app.route('/download-file/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

