import { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [storyIdea, setStoryIdea] = useState('')
  const [genre, setGenre] = useState('Drama')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/generate`, {
        storyIdea,
        genre
      })
      setResult(response.data)
    } catch (err) {
      setError(err.message || 'Failed to generate screenplay')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1 className="title">🎬 Scriptoria</h1>
        <p className="subtitle">AI-Powered Film Pre-Production</p>
      </header>

      <form className="form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="storyIdea" className="label">
            Your Story Idea
          </label>
          <textarea
            id="storyIdea"
            className="textarea"
            rows="5"
            value={storyIdea}
            onChange={(e) => setStoryIdea(e.target.value)}
            placeholder="Describe your story idea in a few sentences..."
            required
            minLength={20}
            maxLength={500}
          />
          <span className="char-count">{storyIdea.length}/500</span>
        </div>

        <div className="form-group">
          <label htmlFor="genre" className="label">
            Genre
          </label>
          <select
            id="genre"
            className="select"
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
          >
            <option value="Drama">Drama</option>
            <option value="Thriller">Thriller</option>
            <option value="Comedy">Comedy</option>
            <option value="Sci-Fi">Sci-Fi</option>
            <option value="Horror">Horror</option>
            <option value="Romance">Romance</option>
          </select>
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? '✨ Generating...' : '🚀 Generate Screenplay'}
        </button>
      </form>

      {error && (
        <div className="error-box">
          <p>❌ {error}</p>
          <p className="error-hint">Make sure the backend server is running on port 5000</p>
        </div>
      )}

      {result && result.success && (
        <div className="results">
          <h2 className="results-title">📝 Generated Screenplay</h2>
          
          <div className="result-section">
            <h3 className="section-title">Title</h3>
            <p className="screenplay-title">{result.screenplay.title}</p>
          </div>

          <div className="result-section">
            <h3 className="section-title">Logline</h3>
            <p>{result.screenplay.logline}</p>
          </div>

          <div className="result-section">
            <h3 className="section-title">Three-Act Structure</h3>
            {Object.entries(result.screenplay.threeActStructure).map(([key, act]) => (
              <div key={key} className="act-box">
                <h4 className="act-title">{act.title}</h4>
                <p className="act-description">{act.description}</p>
                <ul className="act-events">
                  {act.keyEvents.map((event, idx) => (
                    <li key={idx}>{event}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="result-section">
            <h3 className="section-title">Characters</h3>
            <div className="characters-grid">
              {result.characters.map((char, idx) => (
                <div key={idx} className="character-card">
                  <h4 className="char-name">{char.name}</h4>
                  <p className="char-role">{char.role}</p>
                  <p className="char-arc">{char.arc}</p>
                  <div className="char-traits">
                    {char.traits.map((trait, i) => (
                      <span key={i} className="trait-tag">{trait}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
