from flask import Flask, request, jsonify, send_file
from pytubefix import YouTube
import os
import re
import subprocess
import tempfile

app = Flask(__name__)

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def convert_to_mp3(input_file):
    ffmpeg_path = "/usr/bin/ffmpeg"  # Cambia la ruta de FFmpeg si es necesario
    output_file = os.path.splitext(input_file)[0] + '.mp3'
    try:
        subprocess.run([ffmpeg_path, "-i", input_file, "-vn", output_file], check=True)
        os.remove(input_file)  # Elimina el archivo original después de la conversión
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error durante la conversión a MP3: {e}")
        return None

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format = request.args.get('format', 'mp4')

    if not url:
        return jsonify({"message": "Por favor, proporciona una URL válida."}), 400

    try:
        yt = YouTube(url)
        is_audio = (format == "mp3")
        stream = yt.streams.filter(only_audio=is_audio, file_extension="mp4" if not is_audio else None).first()

        if stream:
            sanitized_title = sanitize_filename(yt.title)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Download the file to a temporary location
                download_path = temp_file.name
                stream.download(output_path=os.path.dirname(download_path), filename=os.path.basename(download_path))

                # If the format is mp3, convert the downloaded file
                if is_audio:
                    mp3_path = convert_to_mp3(download_path)
                    if mp3_path:
                        return send_file(mp3_path, as_attachment=True, download_name=f"{sanitized_title}.mp3")
                    else:
                        return jsonify({"message": "Error durante la conversión a MP3."}), 500

                return send_file(download_path, as_attachment=True, download_name=f"{sanitized_title}.mp4")

        else:
            return jsonify({"message": "No se encontraron flujos de video o audio para el formato seleccionado."}), 404

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
