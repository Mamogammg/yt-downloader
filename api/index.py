from flask import Flask, request, jsonify, send_file
from pytubefix import YouTube
import tempfile
import os
import re

app = Flask(__name__)

def sanitize_filename(filename):
    # Remove invalid characters for filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url', 'MWEB')
    format = request.args.get('format', 'mp4')

    if not url:
        return jsonify({"message": "Por favor, proporciona una URL válida."}), 400

    try:
        yt = YouTube(url)
        is_audio = (format == "mp3")  # This line is kept for reference, but will not be used.
        stream = yt.streams.filter(file_extension=format).first()  # Directly filter by requested format

        if stream:
            sanitized_title = sanitize_filename(yt.title)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                download_path = temp_file.name
                stream.download(output_path=os.path.dirname(download_path), filename=os.path.basename(download_path))
                return send_file(download_path, as_attachment=True, download_name=f"{sanitized_title}.{format}")

        else:
            return jsonify({"message": "No se encontraron flujos de video para el formato seleccionado."}), 404

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Main execution for local testing
if __name__ == "__main__":
    app.run(debug=True)
