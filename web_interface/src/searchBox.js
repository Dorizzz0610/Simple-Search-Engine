import React, { useState } from 'react'
import './searchBox.css'

function SearchBox(props) {
  const [inputText, setInputText] = useState('')

  function handleInputChange(event) {
    setInputText(event.target.value)
  }

  function handleSubmit(event) {
    event.preventDefault()
    props.onSubmit(inputText)
  }

  return (
    <form className="search-box" onSubmit={handleSubmit}>
      <label>
        Enter your keywords for searching:
        <input type="text" value={inputText} onChange={handleInputChange} />
      </label>
      <button type="submit">Submit</button>
    </form>
  )
}

export default SearchBox
