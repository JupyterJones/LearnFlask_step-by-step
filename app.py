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
            save_results_to_html(search_results, search_query)

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
            DATA = response.json()
            ic("DATA: ",DATA)
            # Extract search results
            Results = []

            # Check if there are related topics (e.g., disambiguation topics)
            for data in DATA:
                try:
                     ic("DATA: ",data)
                     for resultz in data['Results'][:limit]:
                          ic("RESULT: ",resultz)
                          title = resultz.get('Text', '')
                          url = resultz.get('FirstURL', '')
                          abstract = resultz.get('Abstract', '')
                          text = resultz.get('AbstractText', '')
                          result = resultz.get('Result', '')
                          Results.append({'Title': title, 'URL': url, 'Abstract': abstract, 'AbstractText': text, 'Result': result})
                except:
                     pass          
            ic("XXXXX_ALL_Results: ",Results)
            return Results

        else:
            print(f"Failed to perform DuckDuckGo search. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")



def save_results_to_html(search_results, search_query):
    # Get the current date and time as a string
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a filename based on the current date and time
    filename = f"static/html/search_results_{current_datetime}XX.html"
    with open(filename, 'w') as html_file:
        html_file.write(f"<h1>Search results for '{search_query}'</h1>")
    RESULT=[] 
    for result in search_results:
        html_file.write(f"<h1>'{result}'</h1>")
        html_file.write(f"<h1>'{str(RESULT)}'</h1>")
        RESULT.append(result)
    # Create an HTML file and write the search results to it
    file_name = f"static/html/search_results_{current_datetime}__.html"
    with open(file_name, 'w') as html_file:
        html_file.write(f"<h1>Search results for '{search_query}'</h1>")
        html_file.write("<ul>")
        for result in RESULT:
            html_file.write(f"<li><a href='{result['URL']}'>{result['Title']}</a></li>")
            html_file.write(f"<li>{result['Text']}</li><br>")
            html_file.write(f"<li>{result['FirstURL']}</li><br>")
            html_file.write(f"<li>{result['Abstract']}</li><br>")
            html_file.write(f"<li>'_____This is a line with no meaning_____'</li><br>")
            html_file.write(f"<li>{result['AbstractText']}</li><br>")
            html_file.write(f"<li>{result['Result',]}</li><br>")
            html_file.write("</ul>")
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
