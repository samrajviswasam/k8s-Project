import React from "react";
import "./App.css";

function App() {
  const title = "SAM SJ";
  const version = process.env.REACT_APP_VERSION || "1.0.0";

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div className="logo">
          <span className="logo-icon">☸</span>
          <span>DevOps Platform</span>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>

      {/* Main Content */}
      <main className="container">

        {/* Hero */}
        <section className="hero">
          <div className="hero-badge">
            KUBERNETES APPLICATION
          </div>

          <h1>{title}</h1>

          <p>
            Containerized application deployed using modern
            DevOps practices and Kubernetes.
          </p>
        </section>

        {/* Status Cards */}
        <section className="status-grid">

          <div className="card">
            <div className="card-icon">⚛</div>
            <div>
              <h3>Frontend</h3>
              <span className="running">● Running</span>
            </div>
          </div>

          <div className="card">
            <div className="card-icon">⚙</div>
            <div>
              <h3>Backend</h3>
              <span className="running">● Running</span>
            </div>
          </div>

          <div className="card">
            <div className="card-icon">🗄</div>
            <div>
              <h3>Database</h3>
              <span className="checking">● Checking</span>
            </div>
          </div>

        </section>

        {/* Application Information */}
        <section className="section">

          <div className="section-title">
            <h2>Application Information</h2>
            <span>ENVIRONMENT</span>
          </div>

          <div className="info-card">

            <div className="info-row">
              <span>Application</span>
              <strong>{title}</strong>
            </div>

            <div className="info-row">
              <span>Version</span>
              <strong>{version}</strong>
            </div>

            <div className="info-row">
              <span>Environment</span>
              <strong>Kubernetes</strong>
            </div>

            <div className="info-row">
              <span>Container Runtime</span>
              <strong>Docker</strong>
            </div>

          </div>

        </section>

        {/* DevOps Pipeline */}
        <section className="section">

          <div className="section-title">
            <h2>DevOps Pipeline</h2>
            <span>CI/CD</span>
          </div>

          <div className="pipeline">

            <div className="pipeline-step">
              <div className="pipeline-icon">⑂</div>
              <strong>Git</strong>
              <small>Source Code</small>
            </div>

            <div className="arrow">→</div>

            <div className="pipeline-step">
              <div className="pipeline-icon">⚡</div>
              <strong>CI/CD</strong>
              <small>Automation</small>
            </div>

            <div className="arrow">→</div>

            <div className="pipeline-step">
              <div className="pipeline-icon">🐳</div>
              <strong>Docker</strong>
              <small>Container</small>
            </div>

            <div className="arrow">→</div>

            <div className="pipeline-step">
              <div className="pipeline-icon">☸</div>
              <strong>Kubernetes</strong>
              <small>Deployment</small>
            </div>

            <div className="arrow">→</div>

            <div className="pipeline-step">
              <div className="pipeline-icon">📊</div>
              <strong>Monitoring</strong>
              <small>Prometheus</small>
            </div>

          </div>

        </section>

      </main>

      {/* Footer */}
      <footer>
        <span>DevOps Kubernetes Project</span>
        <span>Version {version}</span>
      </footer>

    </div>
  );
}

export default App;
