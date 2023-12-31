from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from waitress import serve
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
app.config['CORS_HEADERS'] = 'Content-Type'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json['url']
    resolution = request.json.get('resolution', '720p')
    audio_format = request.json.get('audio_format', 'mp3')

    try:
        yt = YouTube(url)

        video_title = yt.title
        print(yt.title)

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
        
        return Response(
            response=response_file,
            status=200,
            headers={
                'Content-Type': f'audio/{file_extension}',
                'Content-Disposition': f'attachment; filename="{video_title}.{file_extension}"',
                'Video-Title': video_title
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


if __name__ == '__main__':
    # app.run()
    serve(app, host='0.0.0.0', port=5000, threads=1) #WAITRESS!

    # flask_thread = threading.Thread(target=app.run)
    # flask_thread.start()

  
    # frontend_thread = threading.Thread(target=serve_frontend)
    # frontend_thread.start()