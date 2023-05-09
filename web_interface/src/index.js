import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import reportWebVitals from './reportWebVitals'
import SearchBox from './searchBox'
import SearchResult from './searchResult'
import Loading from './Loading'

function App() {
  const [searchResults, setSearchResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchStatus, setSearchStatus] = useState('')
  const [isSearchButtonDisabled, setIsSearchButtonDisabled] = useState(false)

  useEffect(() => {
    return () => {
      setSearchResults([])
    }
  }, [])

  function handleSearchSubmit(data) {
    setIsLoading(true)
    setIsSearchButtonDisabled(true)
    setSearchStatus('Searching...')
    setSearchResults([])

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }

    fetch('http://localhost:5000/search', requestOptions)
      .then((response) => response.json())
      .then((data) => {
        console.log('search_results:', data)
        try {
          setSearchResults(data)
          setSearchStatus('')
          setIsLoading(false)
          setIsSearchButtonDisabled(false)
        } catch (error) {
          console.error('Failed to parse JSON:', error)
        }
      })
      .catch((error) => {
        console.error('Error:', error)
      })
  }

  return (
    <div>
      <SearchBox
        onSubmit={handleSearchSubmit}
        setIsLoading={setIsLoading}
        isSearchButtonDisabled={isSearchButtonDisabled}
      />
      {searchStatus && <div>{searchStatus}</div>}
      {searchResults.length > 0 && <SearchResult results={searchResults} />}
      {isLoading && <Loading />}
    </div>
  )
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
)

reportWebVitals()
