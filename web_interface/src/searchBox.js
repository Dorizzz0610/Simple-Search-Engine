import React, { useState } from 'react'
import './searchBox.css'
import Loading from './Loading'

function SearchBox(props) {
  const [inputText, setInputText] = useState('')
  const [startingURL, setStartingURL] = useState('')
  const [maxPages, setMaxPages] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  function handleInputChange(event) {
    setInputText(event.target.value)
  }

  function handleStartingURLChange(event) {
    setStartingURL(event.target.value)
  }

  function handleMaxPagesChange(event) {
    setMaxPages(event.target.value)
  }

  function handleSubmit(event) {
    event.preventDefault()
    setIsLoading(true)
    const data = {
      query: inputText,
      startingURL: startingURL,
      maxPages: maxPages,
    }
    props.onSubmit(data)
  }

  return (
    <form className="search-box" onSubmit={handleSubmit}>
      <label>
        Enter your keywords for searching:
        <input type="text" value={inputText} onChange={handleInputChange} />
      </label>
      <br />
      <label>
        Enter the starting URL:
        <input
          type="text"
          value={startingURL}
          onChange={handleStartingURLChange}
        />
      </label>
      <br />
      <label>
        Enter the maximum number of pages to search:
        <input type="text" value={maxPages} onChange={handleMaxPagesChange} />
      </label>
      <br />
      <button type="submit" disabled={props.isSearchButtonDisabled}>
        Submit
      </button>
      {isLoading && <Loading />}
    </form>
  )
}

export default SearchBox
