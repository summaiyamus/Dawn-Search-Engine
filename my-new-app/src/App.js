// src/App.js
import React from 'react';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <div className="content">
        <h1 className="app-heading">Dawn News Search Engine</h1>
        <SearchBar />
      </div>
    </div>
  );
}

export default App;
