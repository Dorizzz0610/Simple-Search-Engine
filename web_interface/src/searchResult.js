import React from 'react'

function SearchResult(props) {
  const { results } = props
  return (
    <div>
      {results.map((stringList, index) => (
        <ul key={index}>
          {stringList.map((string, i) => (
            <p
              key={i}
              style={{
                fontWeight: i === 0 ? 'bold' : 'normal',
                fontSize: i === 0 ? '20px' : '16px',
              }}
            >
              {string}
            </p>
          ))}
        </ul>
      ))}
    </div>
  )
}

export default SearchResult
