import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <h1>AI Website Builder</h1>
        <p>Coming Soon...</p>
        <Routes>
          <Route path="/" element={<div>Home</div>} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
