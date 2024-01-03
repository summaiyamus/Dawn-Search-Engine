import logging
from flask import Flask, request, jsonify
from main import inverted_index, document_links, search
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

@app.route('/search', methods=['POST'])
def search_handler():
    try:
        print("Received a search request.")
        data = request.get_json()
        print(f"Received data: {data}")
        query = data.get('query')

        if not query:
            raise ValueError("Query is missing. Please enter a query.")

        # Call your existing search function
        results, total_relevant_results = search(query, inverted_index, document_links)

        # Log the results before returning
        print(f"Search results: {results}")
        print(f"Total relevant results: {total_relevant_results}")

        response_data = {
            'status': 'success',
            'results': results,
            'total_results': total_relevant_results
        }

        return jsonify(response_data)

    except ValueError as ve:
        print(f"ValueError during search: {ve}")
        return jsonify({"status": "error", "message": str(ve)})

    except Exception as e:
        print(f"Error during search: {e}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
