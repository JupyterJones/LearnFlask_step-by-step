from flask import Flask, request, render_template, redirect, url_for
import requests
import datetime
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

        # Perform the DuckDuckGo search and get search results
        search_results = perform_duckduckgo_search(search_query)
        ic("search_results: ",search_results)
        # Check if there are search results
        if search_results:
            # Create an HTML file and write the search results to it
            save_results_to_html(search_results)

            # Return a message or redirect to the HTML file
            return redirect(url_for('show_results'))

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
        't': 'duckduck.py'     # Your application name (replace with a suitable name)
    }

    try:
        # Send a GET request to the DuckDuckGo API
        response = requests.get(api_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            ic("DATA: ",data)
            # Extract search results
            results = []

            # Check if there are related topics (e.g., disambiguation topics)
            if 'Results' in data or 'Abstract' in data:
                #ic("DATA: ",data)
                for result in data['Results'][:limit]:
                    ic("RESULT: ",result)
                    title = result.get('Text', '')
                    url = result.get('FirstURL', '')
                    abstract = result.get('Abstract', '')
                    text = result.get('AbstractText', '')
                    results.append({'Title': title, 'URL': url, 'Abstract': abstract, 'AbstractText': text})
            ic("XXXXX\n\nALL: ",results)
            return results

        else:
            print(f"Failed to perform DuckDuckGo search. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")



def save_results_to_html(search_results):
    # Get the current date and time as a string
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a filename based on the current date and time
    filename = f"static/html/search_results_{current_datetime}.html"
    RESULT=[] 
    for result in search_results:
        RESULT.append(result)
    # Create an HTML file and write the search results to it
    with open(filename, 'w', encoding='utf-8') as html_file:
        html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Search Results</title>\n</head>\n<body>\n")
        html_file.write("<h1>Search Results</h1>\n<ul>\n")
        try:
            cnt=0
            for result in search_results:
                cnt=cnt+1
                ic("RESULT: ",result,"CNT: ",cnt)
                html_file.write(f"<li><a href='{result['URL']}'>{result['Title']}</a></li>\n")
                html_file.write(f"<p><strong>Abstract Source:</strong> {result['Abstract']}</p>\n")
                html_file.write(f"<p><strong>Abstract Text:</strong> {result['AbstractText']}</p>\n")
                html_file.write(f"<p><strong>Abstract URL:</strong> <a href='{result['AbstractURL']}'>{result['AbstractURL']}</a></p>\n")
                html_file.write(f"<p><strong>Answer:</strong> {result['Answer']}</p>\n")
        except Exception as e:
            print(f"An error occurred: {str(e)}")        
        html_file.write("</ul>\n</body>\n</html>")         
    ic('RESULT: ' ,RESULT, 'RESULT[0]: ',RESULT[0] ,len(RESULT))        
    return filename
@app.route('/show_results', methods=['GET'])
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
