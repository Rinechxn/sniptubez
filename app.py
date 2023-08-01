from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from pytube import YouTube
import os
from ffmpy import FFmpeg
import http.server
import socketserver
import threading
import unicodedata
import re
import urllib.parse


app = Flask(__name__)
CORS(app)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def normalize_video_title(video_title):
    normalized_title = unicodedata.normalize('NFKD', video_title).encode('ASCII', 'ignore').decode('ASCII')

    return re.sub(r'[^\x00-\x7F]', '', normalized_title)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json['url']
    resolution = request.json.get('resolution', '720p')
    audio_format = request.json.get('audio_format', 'mp3')

    try:
        yt = YouTube(url)

        video_title = yt.title

        video_title_normalized = normalize_video_title(video_title)

        file_extension = '' 

        if 'video' in audio_format:
            video_stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
            video_stream.download('downloads/')
        elif audio_format == 'flac':
            audio_stream = yt.streams.filter(only_audio=True).filter(file_extension='webm').first()
            audio_stream.download('downloads/')
            convert_to_flac(yt.title)
            file_extension = 'flac'
        elif audio_format == 'mp3':
            audio_stream = yt.streams.filter(only_audio=True).filter(file_extension='mp4').first()
            audio_stream.download('downloads/')
            file_extension = 'mp3'
            convert_to_mp3(yt.title)
        elif audio_format == 'wav':
            audio_stream = yt.streams.filter(only_audio=True).filter(file_extension='webm').first()
            audio_stream.download('downloads/')
            convert_to_wav(yt.title)
            file_extension = 'wav'
        else:
            return jsonify({'error': 'Invalid audio format.'}), 400

        file_path = os.path.join('downloads', f'{video_title}.{file_extension}')
        with open(file_path, 'rb') as file:
            response_file = file.read()

        os.remove(file_path)

        encoded_filename = urllib.parse.quote(f'{video_title_normalized}.{file_extension}')

        return Response(
            response=response_file,
            status=200,
            headers={
                'Content-Type': f'audio/{file_extension}',
                'Content-Disposition': f'attachment; filename*=utf-8\'\'{encoded_filename}',
                'x-video-title': video_title 
            }
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

ffmpeg_path = os.path.join(ROOT_DIR, 'bin') 

def convert_to_flac(title):
    input_file = f"downloads/{title}.webm"
    output_file = f"downloads/{title}.flac"
    ff = FFmpeg(inputs={input_file: None}, outputs={output_file: '-y -c:a flac'})
    ff.run()
    os.remove(input_file)

def convert_to_mp3(title):
    input_file = f"downloads/{title}.mp4"
    output_file = f"downloads/{title}.mp3"
    ff = FFmpeg(inputs={input_file: None}, outputs={output_file: '-y -vn -c:a libmp3lame -r 48000 -ab 320k'})
    ff.run()
    os.remove(input_file)

def convert_to_wav(title):
    input_file = f"downloads/{title}.webm"
    output_file = f"downloads/{title}.wav"
    ff = FFmpeg(inputs={input_file: None}, outputs={output_file: '-y -c:a pcm_s16le'})
    ff.run()
    os.remove(input_file)

# def serve_frontend():
#     try:
#         PORT = 8000


#         os.chdir(os.path.join(ROOT_DIR, 'web'))


#         handler = http.server.SimpleHTTPRequestHandler
#         with socketserver.TCPServer(("", PORT), handler) as httpd:
#             print(f"Frontend server running on http://localhost:{PORT}/")
#             httpd.serve_forever()
#     except Exception as e:
#         print(f"Error serving frontend: {str(e)}")

if __name__ == '__main__':
    app.run()

    # flask_thread = threading.Thread(target=app.run)
    # flask_thread.start()

  
    # frontend_thread = threading.Thread(target=serve_frontend)
    # frontend_thread.start()