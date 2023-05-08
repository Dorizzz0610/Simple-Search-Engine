import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import reportWebVitals from './reportWebVitals'
import SearchBox from './searchBox'
import SearchResult from './searchResult'

import io from 'socket.io-client'

const socket = io('http://localhost:5000')

function App() {
  const [searchResults, setSearchResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchStatus, setSearchStatus] = useState('')

  useEffect(() => {
    socket.on('search_start', () => {
      setSearchStatus('Searching...')
      setIsLoading(true)
    })
    socket.on('search_results', (results) => {
      console.log('search_results:', results)
      try {
        setSearchResults(JSON.parse(results))
        setSearchStatus('')
        setIsLoading(false)
      } catch (error) {
        console.error('Failed to parse JSON:', error)
      }
    })

    return () => {
      socket.off('search_start')
      socket.off('search_results')
    }
  }, [])

  function handleSearchSubmit(searchText) {
    socket.emit('search', searchText)
  }

  return (
    <div>
      <SearchBox onSubmit={handleSearchSubmit} setIsLoading={setIsLoading} />
      {searchStatus && <div>{searchStatus}</div>}
      <SearchResult results={searchResults} />
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
