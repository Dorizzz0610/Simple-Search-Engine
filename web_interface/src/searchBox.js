import React, { useState } from 'react'
import './searchBox.css'
import Loading from './Loading'

function SearchBox(props) {
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  function handleInputChange(event) {
    setInputText(event.target.value)
  }

  function handleSubmit(event) {
    event.preventDefault()
    setIsLoading(true)
    props.onSubmit(inputText)
  }

  return (
    <form className="search-box" onSubmit={handleSubmit}>
      <label>
        Enter your keywords for searching:
        <input type="text" value={inputText} onChange={handleInputChange} />
      </label>
      <button type="submit">Submit</button>
      {isLoading && <Loading />}
    </form>
  )
}

export default SearchBox
