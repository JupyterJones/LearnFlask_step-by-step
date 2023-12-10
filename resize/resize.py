# /resize/resize.py
from flask import Flask, render_template, request, send_file, Blueprint, url_for
from PIL import Image
import os
import shutil
import datetime
import logging
from icecream import ic
from logging.handlers import RotatingFileHandler

# Configure this files logger Configure logging
current_dir = os.getcwd()+'/resize/resize.log'
ic ("Current working directory: {0}".format(current_dir))
# Create a file handler to write log messages to a single file with rotation
file_handler = RotatingFileHandler(current_dir, maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 


# Set the formatter for log messages
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')

file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Initialize the Flask app
# Create a Flask app
resize_bp = Blueprint("resize", __name__, template_folder="templates", static_folder="static", static_url_path="assets", url_prefix="/resize")
#
# Define a route for the index page
@resize_bp.route('/')
def resize_index():
    return render_template('resize_index.html')

# Define a route for image resizing
@resize_bp.route('/resize_image', methods=['POST'])
def resize_image():
    try:
        os.makedirs('static/images/resized', exist_ok=True)
        # Access the uploaded image
        uploaded_image = request.files['image']
        
        # Check if no file is selected
        if uploaded_image.filename == '':
            return "No file selected. Please choose an image."
        
        # Open the image using Pillow
        image = Image.open(uploaded_image)
        
        # Get the desired width and height from the form submission
        desired_width = int(request.form['desired_width'])
        desired_height = int(request.form['desired_height'])
        
        # Define the path to save the resized image
        save_path = 'static/images/resized/resized_image.jpg'
        
        # Resize the image to the desired dimensions
        resized_image = image.resize((desired_width, desired_height))
        
        # Save the resized image
        resized_image.save(save_path)
        filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+"_"+str(desired_width)+"X"+str(desired_height)+".jpg"
        shutil.copy(save_path, "static/images/resized/"+filename)

        # Log the save path after it's assigned
        logger.info("Save path: {0}".format(save_path)) 
        
        # Return the resized image as a response
        return render_template('resize_image.html', image=url_for('static', filename='images/resized/' + filename))
    
    except Exception as e:
        return render_template('resize_image.html', image=url_for('static', filename='images/resized/' + filename))
