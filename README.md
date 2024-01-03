## How to Run Code in Your System?

### Backend Setup

1. Install Python version 3.9.

2. Install the following Python packages using pip:
    ```bash
    pip install requests
    pip install beautifulsoup4
    pip install nltk
    pip install pandas
    pip install Flask
    pip install Flask-CORS
    ```

3. Download NLTK resources:
    ```bash
    python -m nltk.downloader stopwords
    python -m nltk.downloader punkt
    ```

### Frontend Setup

1. Install Node.js version v20.10.0 and npm from the official website: [Node.js](https://nodejs.org/).

2. Set up the frontend using the following commands:
    ```bash
    npx create-react-app search-engine-frontend
    cd search-engine-frontend
    npm install
    npm install axios
    npm start
    ```

### Verify Installation

To verify the installations, execute the following commands in the terminal:
```bash
node -v
v20.10.0

npm -v
10.2.5
