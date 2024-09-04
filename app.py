from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import instaloader
import requests
import os 

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend

@app.route('/download-reel', methods=['POST'])
def download_reel():
    data = request.get_json()
    url = data.get('link')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        loader = instaloader.Instaloader()

        # Assuming the URL is of the format: https://www.instagram.com/reel/XYZ/
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Get the URL of the video file
        video_url = post.video_url

        # Stream the video content directly from Instagram
        video_response = requests.get(video_url, stream=True)
        return Response(video_response.iter_content(chunk_size=10*1024),
                        content_type='video/mp4')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
