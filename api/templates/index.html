from flask import Flask, request, render_template, redirect, url_for, send_file
import yt_dlp
import os
import tempfile
import re

app = Flask(__name__)

# Función para limpiar nombres de archivo
def sanitize_filename(filename):
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    # Obtener la URL del video desde el formulario
    video_url = request.form.get('url')

    if not video_url:
        return render_template('index.html', error='Falta el parámetro "url" en la solicitud')

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
                return render_template('index.html', error='El video no se pudo descargar.')

            # Redirigir a una página de descarga
            return render_template('download.html', video_path=video_path, video_title=video_title)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
