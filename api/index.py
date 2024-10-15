from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
from time import sleep

app = Flask(__name__)

# Directorio temporal donde se guardan los videos descargados
DOWNLOAD_DIR = 'downloads'

# Crear el directorio si no existe
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/download', methods=['GET'])
def download_video():
    # Obtener el parámetro URL de la consulta
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({'error': 'Falta el parámetro "url" en la consulta'}), 400

    try:
        # Opciones de descarga para yt-dlp
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'format': 'best',  # Descargar la mejor calidad disponible
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'video')
            video_ext = info_dict.get('ext', 'mp4')
            video_filename = f"{video_title}.{video_ext}"
            video_path = os.path.join(DOWNLOAD_DIR, video_filename)

        sleep(5)

        # Devolver el archivo al cliente
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
