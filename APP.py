from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import datetime
from icecream import ic
import json
import os

app = Flask(__name__)

# Define the name of the JSON file to store results
RESULTS_JSON_FILE = 'results_json.json'

@app.route('/', methods=['GET', 'POST'])
def duckduckgo():
    if request.method == 'POST':
        # Get the search query from the form
        search_query = request.form['search_query']

        # Perform the DuckDuckGo search and get search results
        search_results = perform_duckduckgo_search(search_query)

        # Check if there are search results
        if search_results:
            # Create an HTML file and write the search results to it
            filename = save_results_to_html(search_results, search_query)

            # Return the path to the HTML file for display
            return redirect(url_for('show_results', filename=filename))

    # Render the search form initially
    return render_template('duck_duck_go.html')

def perform_duckduckgo_search(query):
    # Define the DuckDuckGo API endpoint
    api_url = "https://api.duckduckgo.com/"

    # Parameters for the search query
    params = {
        'q': query,
        'format': 'json',
        'no_redirect': 1,
        't': 'duckduck.py'
    }

    try:
        # Send a GET request to the DuckDuckGo API
        response = requests.get(api_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Save the entire response to the JSON file
            save_results_to_json(data)

            return data  # Return the entire response as-is

        else:
            print(f"Failed to perform DuckDuckGo search. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Modify the save_results_to_json function to save the entire response
def save_results_to_json(data):
    try:
        # Open the JSON file in write mode and save the entire response
        with open(RESULTS_JSON_FILE, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Saved entire response to {RESULTS_JSON_FILE}")

    except Exception as e:
        print(f"An error occurred while saving the JSON file: {str(e)}")


def save_results_to_html(search_results, search_query):
    # Get the current date and time as a string
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a filename based on the current date and time
    file_name = f"static/html/search_results_{current_datetime}.html"

    try:
        with open(file_name, 'w') as html_file:
            # Write the HTML header
            html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Search Results</title>\n</head>\n<body>\n")
            html_file.write(f"<h1>Search results for '{search_query}'</h1>\n<ul>\n")

            # Iterate through search results and write each result as an HTML list item
            for result in search_results:
                html_file.write(f"<li><a href='{result['URL']}'>{result['Title']}</a></li>\n")
                html_file.write(f"<li>{result['Text']}</li>\n")
                html_file.write(f"<li>{result['FirstURL']}</li>\n")
                html_file.write(f"<li>{result['Abstract']}</li>\n")
                html_file.write(f"<li>'_____This is a line with no meaning_____'</li>\n")
                html_file.write(f"<li>{result['AbstractText']}</li>\n")
                html_file.write(f"<li>{result['Result']}</li>\n")

            # Write the HTML footer
            html_file.write("</ul>\n</body>\n</html>\n")

        return file_name

    except Exception as e:
        print(f"An error occurred while saving the HTML file: {str(e)}")

@app.route('/show_results', methods=['GET'])
def show_results():
    try:
        # Load the saved JSON data from the file
        with open(RESULTS_JSON_FILE, 'r') as json_file:
            json_data = json.load(json_file)

        # Display the JSON data as a response
        return jsonify(json_data)

    except Exception as e:
        print(f"An error occurred while reading the JSON file: {str(e)}")
        return "Error: Could not read JSON file."


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5500)
