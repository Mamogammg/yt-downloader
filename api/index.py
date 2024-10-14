from flask import Flask, request, jsonify
from pytube import YouTube
import os
import re
import subprocess

app = Flask(__name__)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def convert_to_mp3(input_file, output_file):
    ffmpeg_path = "/usr/bin/ffmpeg"  # Cambia la ruta de FFmpeg si es necesario
    try:
        subprocess.run([ffmpeg_path, "-i", input_file, "-vn", output_file], check=True)
        os.remove(input_file)
    except subprocess.CalledProcessError as e:
        print(f"Error durante la conversión a MP3: {e}")

def descargar_video(url, download_dir, format):
    try:
        yt = YouTube(url)
        is_audio = (format == "mp3")
        stream = yt.streams.filter(only_audio=is_audio, file_extension="mp4" if not is_audio else None).first()

        if stream:
            sanitized_title = sanitize_filename(yt.title)
            original_extension = "webm" if is_audio else "mp4"
            filename = f"{sanitized_title}.{original_extension}"
            download_path = os.path.join(download_dir, filename)
            stream.download(output_path=download_dir, filename=filename)

            if is_audio:
                mp3_filename = f"{sanitized_title}.mp3"
                mp3_path = os.path.join(download_dir, mp3_filename)
                convert_to_mp3(download_path, mp3_path)

            return f"Archivo descargado: {sanitized_title}"
        else:
            return "No se encontraron flujos de video o audio para el formato seleccionado."
    except Exception as e:
        return f"Error: {e}"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format = request.args.get('format', 'mp4')
    download_dir = os.path.expanduser("~/downloads")

    if url:
        resultado = descargar_video(url, download_dir, format)
        return jsonify({"message": resultado})
    else:
        return jsonify({"message": "Por favor, proporciona una URL válida."})

if __name__ == '__main__':
    app.run(debug=True)
