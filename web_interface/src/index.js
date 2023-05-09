import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import reportWebVitals from './reportWebVitals'
import SearchBox from './searchBox'
import SearchResult from './searchResult'
import Loading from './Loading'

import io from 'socket.io-client'

const socket = io('http://localhost:5000')

function App() {
  const [searchResults, setSearchResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchStatus, setSearchStatus] = useState('')
  const [isSearchButtonDisabled, setIsSearchButtonDisabled] = useState(false)

  useEffect(() => {
    socket.on('search_start', () => {
      setSearchStatus('Searching...')
      setIsLoading(true)
      setIsSearchButtonDisabled(true)
    })
    socket.on('search_results', (results) => {
      console.log('search_results:', results)
      try {
        setSearchResults(JSON.parse(results))
        setSearchStatus('')
        setIsLoading(false)
        setIsSearchButtonDisabled(false)
      } catch (error) {
        console.error('Failed to parse JSON:', error)
      }
    })

    return () => {
      socket.off('search_start')
      socket.off('search_results')
    }
  }, [])

  function handleSearchSubmit(data) {
    setSearchResults([])
    socket.emit('search', data)
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
