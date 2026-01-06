import React from 'react';
import ImageUpload from './components/ImageUpload';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">D</div>
            <span>DermaInspect</span>
          </div>
          <nav>
            <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              AI-Powered Leprosy Detection
            </span>
          </nav>
        </div>
      </header>
      
      <main className="app-main">
        <ImageUpload />
      </main>
      
      <footer className="app-footer">
        <div className="footer-content">
          <p>
            <strong>Medical Disclaimer:</strong> This tool is for research and educational purposes only.
            It is not a substitute for professional medical diagnosis, advice, or treatment.
          </p>
          <p style={{ marginTop: '0.5rem', fontSize: '0.75rem' }}>
            Always consult a qualified healthcare professional for proper diagnosis and treatment.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
