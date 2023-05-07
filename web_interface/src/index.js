import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'
import reportWebVitals from './reportWebVitals'
import SearchBox from './searchBox'

function handleSearchSubmit(searchText) {
  fetch('/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ searchText: searchText }),
  })
    .then((response) => response.text())
    .then((result) => {
      console.log(result)
    })
    .catch((error) => {
      console.error(error)
    })
}

ReactDOM.render(
  <React.StrictMode>
    <SearchBox onSubmit={handleSearchSubmit} />
  </React.StrictMode>,
  document.getElementById('root')
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
