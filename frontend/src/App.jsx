import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './index.css';

const API_BASE = 'http://localhost:5000';

function App() {
  const [storyIdea, setStoryIdea] = useState('');
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('Outline');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [runtime, setRuntime] = useState(0);
  const timerRef = useRef(null);

  useEffect(() => {
    if (loading) {
      timerRef.current = setInterval(() => {
        setRuntime(t => t + 1);
      }, 1000);
    } else {
      clearInterval(timerRef.current);
    }
    return () => clearInterval(timerRef.current);
  }, [loading]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.pdf') && !file.name.endsWith('.docx')) {
      alert('Please upload a PDF or DOCX file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setIsUploading(true);
    setUploadProgress(0);

    try {
      const response = await axios.post(`${API_BASE}/upload`, formData, {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        }
      });

      if (response.data.success) {
        setStoryIdea(response.data.extracted_text);
        alert(`Successfully extracted ${response.data.full_length} characters from ${file.name}`);
      }
    } catch (err) {
      console.error('Upload failed:', err);
      alert(err.response?.data?.error || 'Failed to extract text from file.');
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (loading || storyIdea.length < 20) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setRuntime(0);

    try {
      const response = await axios.post(`${API_BASE}/generate`, {
        storyIdea,
        genre: selectedGenres[0] || 'Drama'
      });
      setResult(response.data);
      setActiveTab('Outline');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.details || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    if (!result) return;
    try {
      const response = await axios.post(`${API_BASE}/export_pdf`, result, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Scriptoria_${result.screenplay.title}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Export failed:', err);
      alert('Failed to export PDF');
    }
  };

  const tabs = ['Outline', 'Characters', 'Scenes', 'Sound'];

  return (
    <div className="max-w-4xl mono">
      {/* Header Section */}
      <header>
        <div>
          <h1>New Story</h1>
          <p>Project Initiation Phase • v.1.0</p>
        </div>
        <div className="header-icons">
          <button style={{ background: 'none', border: 'none', cursor: 'pointer' }} onClick={() => window.location.reload()}>⟲</button>
          <button style={{ background: 'none', border: 'none', cursor: 'pointer' }}>⟳</button>
        </div>
      </header>

      <main>
        {!result ? (
          <div className="animate-fade-in">
            {/* Main Input Card */}
            <div className="retro-card">
              <div className="card-dots">
                <div className="dot" />
                <div className="dot" />
                <div className="dot" />
              </div>
              <div className="card-content">
                <div className="card-label">Untitled Project</div>
                <textarea
                  className="lined-paper"
                  placeholder="Start typing your logline or synopsis here..."
                  value={storyIdea}
                  onChange={(e) => setStoryIdea(e.target.value)}
                  disabled={loading || isUploading}
                />
              </div>
            </div>

            {/* Action Grid */}
            <div className="action-grid">
              {/* Upload Box */}
              <label className="upload-box">
                <input type="file" className="hidden" style={{ display: 'none' }} accept=".pdf,.docx,.doc" onChange={handleFileUpload} />
                <div className="upload-icon">
                  {isUploading ? '⌛' : '☁'}
                </div>
                <div className="upload-text">
                  <b>Upload Script</b>
                  <span>.PDF, .FDX, .TXT</span>
                </div>
                {uploadProgress > 0 && (
                  <div style={{ width: '100%', height: '2px', background: '#eee', marginTop: '10px' }}>
                    <div style={{ width: `${uploadProgress}%`, height: '100%', background: 'black' }} />
                  </div>
                )}
              </label>

              {/* Settings Box */}
              <div className="settings-box">
                <div>
                  <div className="label-small">Select Genre</div>
                  <div className="select-wrapper">
                    <select
                      value=""
                      onChange={(e) => {
                        const val = e.target.value;
                        if (val && !selectedGenres.includes(val)) {
                          setSelectedGenres([...selectedGenres, val]);
                        }
                      }}
                    >
                      <option value="">Add Genre...</option>
                      <option>Drama</option>
                      <option>Thriller</option>
                      <option>Comedy</option>
                      <option>Sci-Fi</option>
                      <option>Horror</option>
                    </select>
                    <div className="select-arrow">▼</div>
                  </div>
                </div>

                <div className="tag-row">
                  {selectedGenres.map(g => (
                    <div key={g} className="tag tag-blue">
                      {g}
                      <button onClick={() => setSelectedGenres(selectedGenres.filter(x => x !== g))}>×</button>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={loading || storyIdea.length < 20}
              className="btn-primary"
            >
              {loading ? `${runtime}s Processing...` : 'Generate Breakdown'}
            </button>

            {error && (
              <div style={{ textAlign: 'center', color: '#d36d5b', border: '2px solid #d36d5b', padding: '16px', fontWeight: '900', marginTop: '20px' }}>
                ⚠️ {error}
              </div>
            )}
          </div>
        ) : (
          <div className="animate-fade-in">
            {/* Results Nav Header */}
            <div className="tabs-container">
              <div className="tabs-group">
                {tabs.map(tab => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
              <button
                onClick={handleExportPDF}
                className="btn-export"
              >
                Export Package (PDF)
              </button>
            </div>

            {/* Content Display */}
            <div className="result-content">
              {activeTab === 'Outline' && (
                <div className="animate-fade-in">
                  <div style={{ borderBottom: '4px solid black', paddingBottom: '20px', marginBottom: '40px' }}>
                    <h2 style={{ fontSize: '36px', fontWeight: '900', textTransform: 'uppercase' }}>{result.screenplay.title}</h2>
                    <p style={{ opacity: 0.7, fontStyle: 'italic', fontWeight: '600' }}>"{result.screenplay.logline}"</p>
                    {result.screenplay.mainCharacters && result.screenplay.mainCharacters.length > 0 && (
                      <div style={{ marginTop: '16px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                        <span style={{ fontSize: '11px', fontWeight: '900', textTransform: 'uppercase', color: '#888' }}>Cast:</span>
                        {result.screenplay.mainCharacters.map((char, idx) => (
                          <span key={idx} className="tag tag-teal">{char}</span>
                        ))}
                      </div>
                    )}
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '40px' }}>
                    {Object.entries(result.screenplay.threeActStructure).map(([key, act]) => (
                      <div key={key}>
                        <span className="act-tag">{key}</span>
                        <h3 style={{ fontSize: '20px', borderBottom: '1px solid black', paddingBottom: '8px', marginBottom: '16px' }}>{act.title}</h3>
                        <p style={{ fontSize: '14px', fontWeight: '600', opacity: 0.8, lineHeight: 1.6 }}>{act.description}</p>
                        <ul style={{ listStyle: 'none', marginTop: '16px' }}>
                          {act.keyEvents.map((event, i) => (
                            <li key={i} style={{ fontSize: '12px', fontWeight: '700', marginBottom: '8px', display: 'flex', gap: '8px' }}>• <span>{event}</span></li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'Characters' && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }} className="animate-fade-in">
                  {result.characters.map((char, idx) => (
                    <div key={idx} style={{ border: '2px solid black', padding: '24px', background: '#f9f9f9', boxShadow: '4px 4px 0 black' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid black', paddingBottom: '8px' }}>
                        <h3 style={{ fontSize: '24px', fontWeight: '900' }}>{char.name}</h3>
                        <span style={{ fontSize: '10px', fontWeight: '900', background: 'white', border: '1px solid black', padding: '4px 8px' }}>{char.role}</span>
                      </div>
                      <p style={{ fontSize: '14px', fontWeight: '700', opacity: 0.8, fontStyle: 'italic' }}>{char.arc}</p>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '24px' }}>
                        {char.traits.map(trait => (
                          <span key={trait} className="tag tag-teal">{trait}</span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'Scenes' && (
                <div className="animate-fade-in">
                  {result.scenes.map((scene, idx) => (
                    <div key={idx} style={{ display: 'flex', gap: '24px', borderBottom: '1px solid #eee', paddingBottom: '32px', marginBottom: '32px' }}>
                      <div style={{ fontSize: '40px', fontWeight: '900', color: '#eee', width: '60px', textDecoration: 'underline', textDecorationThickness: '4px', textUnderlineOffset: '8px' }}>
                        {scene.sceneNumber.toString().padStart(2, '0')}
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '12px' }}>
                          <span style={{ fontWeight: '900', textTransform: 'uppercase', fontSize: '14px', border: '2px solid black', padding: '0 8px' }}>{scene.location}</span>
                          <span style={{ fontWeight: '700', textTransform: 'uppercase', fontSize: '12px', opacity: 0.5 }}>{scene.timeOfDay}</span>
                        </div>
                        <p style={{ fontWeight: '700', fontSize: '18px' }}>{scene.action}</p>
                        <div style={{ fontSize: '10px', fontWeight: '900', color: '#aaa', marginTop: '12px' }}>
                          CAST: {scene.characters.join(' / ')}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'Sound' && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '48px' }} className="animate-fade-in">
                  <div>
                    <div style={{ marginBottom: '48px' }}>
                      <h3 className="label-small" style={{ textDecoration: 'underline' }}>Sonic Architecture</h3>
                      <div style={{ fontSize: '32px', fontWeight: '900', textTransform: 'uppercase' }}>{result.soundDesign.musicTheme.style}</div>
                      <p style={{ fontWeight: '700', opacity: 0.6, fontStyle: 'italic' }}>{result.soundDesign.musicTheme.mood}</p>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '16px' }}>
                        {result.soundDesign.musicTheme.instruments.map(inst => (
                          <span key={inst} className="tag tag-blue">{inst}</span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="label-small">Ambiance Map</h3>
                      {result.soundDesign.ambience.map((amb, i) => (
                        <div key={i} style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
                          <div style={{ fontWeight: '900', fontSize: '24px', opacity: 0.2 }}>0{i + 1}</div>
                          <div>
                            <div style={{ fontWeight: '900', textTransform: 'uppercase', fontSize: '14px' }}>{amb.location}</div>
                            <p style={{ fontSize: '12px', fontWeight: '700', opacity: 0.6 }}>{amb.description}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div style={{ background: '#1a1a1a', color: 'white', padding: '32px', boxShadow: '8px 8px 0 #d36d5b' }}>
                    <h3 className="label-small" style={{ color: '#555' }}>Audio Beat-Sheet</h3>
                    <div style={{ marginTop: '32px' }}>
                      {result.soundDesign.keyMoments.map((moment, i) => (
                        <div key={i} style={{ position: 'relative', paddingLeft: '32px', borderLeft: '2px solid #333', paddingBottom: '40px' }}>
                          <div style={{ position: 'absolute', top: 0, left: '-6px', width: '10px', height: '10px', background: '#d36d5b', borderRadius: '50%' }} />
                          <div style={{ fontSize: '10px', fontWeight: '900', color: '#555', marginBottom: '8px' }}>SCN {moment.scene}</div>
                          <div style={{ fontWeight: '700', fontSize: '14px', marginBottom: '8px' }}>{moment.moment}</div>
                          <div style={{ fontSize: '12px', opacity: 0.5, fontStyle: 'italic' }}>// {moment.soundDesign}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Back Button */}
            <div style={{ marginTop: '40px', textAlign: 'center' }}>
              <button
                onClick={() => setResult(null)}
                style={{ background: 'none', border: 'none', borderBottom: '2px solid black', paddingBottom: '4px', fontWeight: '900', fontSize: '11px', textTransform: 'uppercase', cursor: 'pointer' }}
              >
                Reset Workshop
              </button>
            </div>
          </div>
        )}
      </main>

      <footer>
        <span>Scriptoria Process Node 2026</span>
        <span>Transmission: Secured</span>
        <span>Groq: 70B Engine</span>
      </footer>
    </div>
  );
}

export default App;
