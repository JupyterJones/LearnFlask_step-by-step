from flask import Flask, request, render_template
import requests
from icecream import ic
import json

app = Flask(__name__)

# Define the name of the JSON file to store results
RESULTS_JSON_FILE = 'results_json.json'

@app.route('/', methods=['GET', 'POST'])
def duckduckgo():
    if request.method == 'POST':
        # Get the search query from the form
        search_query = request.form['search_query']
        ic(search_query)
        # Perform the DuckDuckGo search and get search results
        search_results = perform_duckduckgo_search(search_query)
        ic(search_results)
        
        # Check if there are search results
        if search_results:
            # Save the entire search response to the JSON file
            save_search_response(search_results)
            
            # Pass the search results to the template for display
            return render_template('results.html', search_results=search_results)
        else:
            # Handle the case when there are no search results
            error_message = "No search results found."
            return render_template('duck_duck_go.html', error_message=error_message)

    # Render the search form initially
    return render_template('duck_duck_go.html')

def perform_duckduckgo_search(query, limit=3):
    # Define the DuckDuckGo API endpoint
    api_url = "https://api.duckduckgo.com/"

    # Parameters for the search query
    params = {
        'q': query,            # The search query
        'format': 'json',      # Response format
        'no_redirect': 1,      # Prevent redirect to external websites
    't': 'duckduck.py'         # Your application name (replace with a suitable name)
    }

    try:
        # Send a GET request to the DuckDuckGo API
        response = requests.get(api_url, params=params)
        ic(response)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            ic(data)
            if 'AbstractURL' in data and len(data['AbstractURL']) > 0:
                # Return the search results
                #return data['Abstract']
                ic(data['Abstract'])
                return data  # Return the entire search response

        else:
            print(f"Failed to perform DuckDuckGo search. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def save_search_response(response):
    # Load existing results if the JSON file exists
    try:
        with open(RESULTS_JSON_FILE, 'r') as json_file:
            existing_results = json.load(json_file)
    except FileNotFoundError:
        existing_results = []

    # Append the new search response to the existing results
    existing_results.append(response)

    # Save the combined results to the JSON file
    with open(RESULTS_JSON_FILE, 'w') as json_file:
        json.dump(existing_results, json_file, indent=4)

@app.route('/results', methods=['GET'])
def show_results():
    try:
        with open('results_json.json', 'r') as json_file:
            search_results = json.load(json_file)
        return render_template('results.html', search_results=search_results)
    except FileNotFoundError:
        error_message = "No search results found."
        return render_template('duck_duck_go.html', error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5500)
