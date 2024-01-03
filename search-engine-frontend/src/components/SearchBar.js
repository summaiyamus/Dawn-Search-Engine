import React, { useState } from 'react';
import axios from 'axios';
import './SearchBar.css'; // Import the CSS file for styling

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [visibleResults, setVisibleResults] = useState(6);
  const [totalResults, setTotalResults] = useState(0);
  const [startTime, setStartTime] = useState(0);
  const [endTime, setEndTime] = useState(0);
  const [error, setError] = useState(null);

const handleSearch = async () => {
  setIsLoading(true);
  setStartTime(performance.now());

  try {
    const response = await axios.post('http://localhost:5000/search', { query });
    console.log('API Response:', response.data); // Log the response

    setResults(response.data.results || []);
    setTotalResults(response.data.results.length);
  } catch (error) {
    console.error('Error fetching search results:', error);
    setError('An error occurred while fetching results.');
  } finally {
    setIsLoading(false);
    setEndTime(performance.now());
  }
};

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleMoreResults = () => {
    setVisibleResults((prevVisibleResults) => prevVisibleResults + 6);
  };

  const calculateElapsedTime = () => {
    const elapsedTimeInSeconds = ((endTime - startTime) / 1000).toFixed(2);
    console.log(`Time taken: ${elapsedTimeInSeconds} seconds | Total Results: ${totalResults}`);
    return elapsedTimeInSeconds;
  };

  return (
    <div className="search-container">
      <div className="search-bar">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter your search query"
        />
        <button onClick={handleSearch} disabled={isLoading}>
          <img
            src="https://www.gstatic.com/images/icons/material/system/2x/search_black_24dp.png"
            alt="Search Icon"
            className="search-icon"
          />
        </button>
      </div>

      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}


      <div className="search-time">
        {startTime > 0 && endTime > 0 && (
          <p>
            Search time: {calculateElapsedTime()} seconds
          </p>
        )}
      </div>

      <ul className="search-results">
        {Array.isArray(results) &&
          results.slice(0, visibleResults).map((result, index) => (
            <li key={index}>
              <h3>
                <a
                  href={result.Link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {result.Heading}
                </a>
              </h3>
              <p className="link">{result.Link}</p>
              <p className="summary">{result.Summary}</p>
            </li>
          ))}
      </ul>

      {totalResults > visibleResults && (
        <button className="more-button" onClick={handleMoreResults}>
          Load More Results
        </button>
      )}
    </div>
  );
};

export default Search;
