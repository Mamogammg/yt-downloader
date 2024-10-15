from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import tempfile
import re

app = Flask(__name__)

# Función para limpiar nombres de archivo
def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

@app.route('/download', methods=['GET'])
def download_video():
    # Obtener la URL del video desde los parámetros de la URL
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({'error': 'Falta el parámetro "url" en la solicitud'}), 400

    try:
        # Crear un directorio temporal para almacenar el video
        with tempfile.TemporaryDirectory() as temp_dir:
            # Opciones de descarga para yt-dlp
            ydl_opts = {
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',  # Descargar en el directorio temporal
                'format': 'best',  # Descargar la mejor calidad disponible
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_title = info_dict.get('title', 'video')
                video_ext = info_dict.get('ext', 'mp4')
                video_filename = f"{sanitize_filename(video_title)}.{video_ext}"
                video_path = os.path.join(temp_dir, video_filename)

            # Verificar si el archivo se descargó correctamente
            if not os.path.exists(video_path):
                return jsonify({'error': f"El archivo {video_filename} no fue encontrado después de la descarga"}), 500

            # Devolver el archivo al cliente
            return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
