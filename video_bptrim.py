#!/home/jack/miniconda3/envs/cloned_base/bin/python
# Import necessary libraries
from flask import Flask, render_template, request, send_file, Blueprint, url_for
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from werkzeug.utils import secure_filename
import os
import logging
import shutil
import datetime
# Create a Flask app
video_bptrim_bp = Blueprint("video_bptrim",__name__)

# Configure logging
log_filename = 'app.log'
log_format = '%(asctime)s [%(levelname)s] - %(message)s'
logging.basicConfig(filename=log_filename, level=logging.ERROR, format=log_format)

# Define the directory where uploaded videos will be stored
UPLOAD_FOLDER = 'static/videos/uploaded/'

# Set allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@video_bptrim_bp.route('/view_vid')
def view_vid():
    # Ensure the directory for storing uploaded videos exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Ensure the directory for saving trimmed videos exists
    os.makedirs('static/videos/uploaded', exist_ok=True)
    os.makedirs('static/videos/trimmed', exist_ok=True)    
    return render_template('view_vid.html')
# Define the route for viewing and trimming video
@video_bptrim_bp.route('/view_and_trim', methods=['GET', 'POST'])
def view_and_trim():
    video_path = None

    if request.method == 'POST':
        # Check if the post request has a file part
        if 'video' not in request.files:
            return "No video file uploaded. Please choose a video."

        uploaded_video = request.files['video']

        # Check if the file is empty
        if uploaded_video.filename == '':
            return "No video file selected. Please choose a video."

        # Check if the file has an allowed extension
        if not allowed_file(uploaded_video.filename):
            return "Invalid video format. Please choose a supported video format."

        # Generate a secure filename and save the uploaded video
        filename = secure_filename(uploaded_video.filename)
        video_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_video.save(video_path)

    return render_template('view_vid.html', video_path=video_path)

# Define the route to handle video trimming
@video_bptrim_bp.route('/trim_video', methods=['POST', 'GET'])
def trim_video():
    try:
        # Access the form values
        start_time = request.form['start_time']
        duration = request.form['duration']
        video_path = request.form['video_path']

        # Define the path to save the trimmed video
        save_path = 'static/videos/trimmed_video.mp4'

        # Use moviepy's ffmpeg_extract_subclip to trim the video
        ffmpeg_extract_subclip(video_path, float(start_time), float(start_time) + float(duration), targetname=save_path)
        filename =datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".mp4"
        logging.info("FILE_NAME: ",filename)
        final ='static/videos/trimmed/'+filename
        logging.info("FINAL_VIDEO_PATH: ",final)
        #            static/videos/trimmed_video.mp4
        #                                               static/videos/trimmed
        # Define the full source and destination paths
        source_path = 'static/videos/trimmed_video.mp4'
        destination_path = os.path.join('static/videos/trimmed', filename)

        # Use shutil.copy to copy the trimmed video to the destination
        shutil.copy(source_path, destination_path)

        # Return the path to the copied video
        final = destination_path
        return render_template('view_vid.html', video_path=final)
    except Exception as e:
        # Log any errors
        logging.error(f"Error while trimming video: {str(e)}")
        return "An error occurred while trimming the video."


 
 
