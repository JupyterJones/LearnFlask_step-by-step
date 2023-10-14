from flask import Flask, request, render_template
import requests
from icecream import ic

app = Flask(__name__)

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
            # Extract search results
            results = []
       
            # Check if there are related topics (e.g., disambiguation topics)
            if 'Results' in data:
                for result in data['Results'][:limit]:
                    title = result.get('Text', '')
                    url = result.get('FirstURL', '')
                    results.append({'Title': title, 'URL': url})
            ic(results)
            return results

        else:
            print(f"Failed to perform DuckDuckGo search. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5500)
