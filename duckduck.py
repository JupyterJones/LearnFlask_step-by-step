from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
import datetime
import json  # Import the json module
import os
import json
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
            # Save the entire response to the JSON file
            save_results_to_json(search_results)

            # Redirect to a page to show the saved JSON file
            return redirect(url_for('show_json_results'))

    # Render the search form initially
    return render_template('duck_duck_go.html')

def perform_duckduckgo_search(query, limit=3):
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

            # Extract search results
            results = []

            if 'Results' in data:
                for result in data['Results'][:limit]:
                    title = result.get('Text', '')
                    url = result.get('FirstURL', '')
                    abstract = result.get('Abstract', '')
                    text = result.get('AbstractText', '')
                    results.append({'Title': title, 'URL': url, 'Abstract': abstract, 'AbstractText': text})

            return results

        else:
            print(f"Failed to perform DuckDuckGo search. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def save_results_to_json(data):
    try:
        # Open the JSON file in write mode and save the entire response
        with open(RESULTS_JSON_FILE, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Saved entire response to {RESULTS_JSON_FILE}")

    except Exception as e:
        print(f"An error occurred while saving the JSON file: {str(e)}")

@app.route('/show_json_results', methods=['GET'])
def show_json_results():
    try:
        with open(RESULTS_JSON_FILE, 'r') as json_file:
            json_data = json.load(json_file)
            return jsonify(json_data)  # Return JSON data as a response

    except Exception as e:
        print(f"An error occurred while reading the JSON file: {str(e)}")
        return "Error: Could not read JSON file."

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5500)
