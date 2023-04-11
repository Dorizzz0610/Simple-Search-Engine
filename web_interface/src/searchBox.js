const [input, setInput] = useState('')

function handleChange(e) {
  setInput(e.target.value)
}

return (
  <div>
    {' '}
    <input
      style={{ width: '500px' }}
      value={input}
      onChange={handleChange}
    />{' '}
  </div>
)
