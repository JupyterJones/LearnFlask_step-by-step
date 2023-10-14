#!/home/jack/Desktop/FlaskAppArchitect_Flask_App_Creator/env/bin/python
import os
import glob
import shutil
import tempfile
import subprocess
import datetime
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, Response, send_file
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.editor import concatenate_videoclips, AudioFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import logging
from time import sleep
from random import randint
from PIL import Image, ImageDraw, ImageFont 
import random
import time
import uuid
import io
import numpy as np
from logging.handlers import RotatingFileHandler
#from zoomin import zoomin_bp
app = Flask(__name__)
app.use_static_path = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file
file_handler = RotatingFileHandler(
    'Logs/app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
logger.info("Logger created")
logger.debug("Test debug message")

# Create a stderr handler to write log messages to sys.stderr
console_handler = logging.StreamHandler()
#app.register_blueprint(zoomin_bp)
@app.route('/favicons.ico')
def favicons():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/favicon.ico')
def favicon():
    # Set the size of the favicon
    size = (16, 16)

    # Create a new image with a transparent background
    favicon = Image.new('RGBA', size, (0, 0, 0, 0))

    # Create a drawing object
    draw = ImageDraw.Draw(favicon)

    # Draw a yellow square
    square_color = (255, 0, 255)
    draw.rectangle([(0, 0), size], fill=square_color)

    # Draw a red circle
    circle_center = (size[0] // 2, size[1] // 2)
    circle_radius = size[0] // 3
    logger.info(f'circle_center, circle_radius:,{circle_center} {circle_radius}')
    circle_color = (255, 255, 0)
    draw.ellipse(
        [(circle_center[0] - circle_radius, circle_center[1] - circle_radius),
         (circle_center[0] + circle_radius, circle_center[1] + circle_radius)],
        fill=circle_color
    )

    # Save the image to a memory buffer
    image_buffer = io.BytesIO()
    favicon.save(image_buffer, format='ICO')
    image_buffer.seek(0)

    return Response(image_buffer.getvalue(), content_type='image/x-icon')


@app.route("/", methods=['POST', 'GET'])
def index():
    CMD = "TEST THIS"
    return render_template("index.html",CMD=CMD)
@app.route("/mpegit" , methods=['POST', 'GET'])
def mpegit():
    video="static/videos/Final2.mp4"
    return render_template("mpegit.html",output_video=video)
@app.route("/command" , methods=['POST', 'GET'])
def command():
    # Input image and output video file names
    input_image = 'static/images/backgrounds/5120x512_joined_image.jpg'
    output_video = input_image[:-4] + '_output.mp4'
    print("OutputVideo: ", output_video)
    # Dimensions of the input image (2400x512)
    input_width = 5120
    input_height = 512
    # Desired output video dimensions (512x512)
    output_width = 512
    output_height = 512
    # Duration of the video in seconds (58 seconds)
    duration = 58
    # Calculate the distance to scroll per frame
    scroll_distance = (input_width - output_width) / (duration * 25)  # Assuming 25 frames per second
    print("Scroll Distance: ", scroll_distance)
    # ffmpeg command to create the video
    command = [
        'FFmpeg', '-hide_banner',
        '-loop', '1', '-i', f'{input_image}',
        '-vf', 'scale=5120:512,scroll=horizontal=0.0001,crop=512:512:0:0,format=yuv420p',
    '-t', f'{duration}', '-y', f'{output_video}',
        ]
    subprocess.run(command)
    output_video2 = 'static/videos/Final2.mp4'
    command2 = [
               
        'FFmpeg', '-hide_banner',
        '-i', f'{output_video}',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '0', '-c:a', 'aac', '-b:a', '192k', '-movflags', 'faststart', '-y', f'{output_video2}'
        ]
    subprocess.run(command2)   

    try:
        logging.info('Creating the video...')
        subprocess.run(command, check=True)
        logging.info(f'Video "{output_video}" created successfully.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error: {e}')

    #view = ["vlc", output_video]
    #subprocess.run(view, check=True)
    video=f'{output_video2}'
    #shutil.copyfile(output_video, 'static/videos/final.mp4')
    #video = 'static/videos/Final2.mp4'
    return redirect(url_for('mpegit',video=video,scroll_distance=scroll_distance))
@app.route("/commando" , methods=['POST', 'GET'])
def commando():
    """
    Generates a video by scrolling a given input image horizontally for a specified duration.
    Args:
        None
    Returns:
        redirect(url_for('mpegit',video=video))
    """
    # Input image and output video file names
    input_image = 'static/images/backgrounds/3400x512.jpg'
    output_video = input_image[:-4] + 'output.mp4'
    print("OutputVideo: ", output_video)
    # Dimensions of the input image (2400x512)
    input_width = 5120
    input_height = 512
    # Desired output video dimensions (512x512)
    output_width = 512
    output_height = 512
    # Duration of the video in seconds (58 seconds)
    duration = 58
    # Calculate the distance to scroll per frame
    scroll_distance = (input_width - output_width) / (duration * 25)  # Assuming 25 frames per second
    # ffmpeg command to create the video
    # ffmpeg command to create the video
    # Define the filter string separately
    # Define the filter string separately
    command2 = [
        'FFmpeg', '-hide_banner',
'-loop', '1', '-i', f"{input_image}",
        '-vf', 'scale=3400:512,scroll=horizontal=0.0001,crop=512:512:0:0,format=yuv420p',
        '-t', '120', '-y', f"{output_video}"
    ]
    subprocess.run(command2)

    try:
        logging.info('Creating the video...')
        subprocess.run(command2, check=True)
        logging.info(f'Video "{output_video}" created successfully.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error: {e}')
    video="static/videos/ThumbNails_Background_FFmpeg2.mp4"
    view = ["vlc", video]
    subprocess.run(view, check=True)

    return redirect(url_for('mpegit',video=video))

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    uploaded_file = request.files['videoFile']
    if uploaded_file.filename != '':
        # Save the uploaded file to a directory or process it as needed
        # For example, you can save it to a specific directory:
        uploaded_file.save('static/uploads/' + uploaded_file.filename)
        return 'File uploaded successfully'
    else:
        return 'No file selected'

# How do I ?
# open the file static/text/flask_notes.txt
# split at the line "----------" 
# SEARCH THE TEXT FOR "uploads"
# print the results on an html page
@app.route('/notes')
def notes():
    with open('static/text/flask_notes.txt') as f:
        text = f.read()
        #paragraph = text.split('----------')
        #search the paragraph for "uploads"

    return render_template('flask_notes.html', text=text)  # split at the line "----------" and return the second part
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        if search_term:
            with open('static/text/flask_notes.txt', 'r') as f:
                text = f.read()
                paragraphs = text.split('----------')

                # Filter paragraphs that contain the search term
                matching_paragraphs = [p for p in paragraphs if search_term in p]

            if matching_paragraphs:
                logger.debug("Matching Paragraphs: ", matching_paragraphs)
                return render_template('flask_notes.html', text=matching_paragraphs)
            else:
                return render_template('flask_notes.html', text=["No matching results."])
        else:
            return render_template('flask_notes.html', text=["Enter a search term."])

    return render_template('flask_notes.html', text=[])

# Function to add ten dashes before and after the content
def format_content(content):
    separator = '----------\n'  # Define the separator
    formatted_content = f'{separator}{content.strip()}'  # Add separator before and after
    return formatted_content

@app.route('/append_notes', methods=['POST', 'GET'])
def append_notes():
    if request.method == 'POST':
        new_content = request.form.get('new_content', '').strip()
        if new_content:
            formatted_content = format_content(new_content)  # Format the content
            with open('static/text/flask_notes.txt', 'a') as f:
                f.write(formatted_content)
            return 'Note appended successfully'
        else:
            return 'No content to append'

    return render_template('append_notes.html')


if __name__ == '__main__':
    print("Starting Python Flask Server For Ffmpeg \n Code Snippets on port 5100")
    app.run(debug=True, host='0.0.0.0', port=5100)
