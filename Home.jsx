
import "./Home.css";

export default function Home({ onNavigate }) {
  return (
    <div className="home-page">
      <header className="home-navbar">
        <a className="home-logo" href="#home">
          <span>CR</span> CivicResolve AI
        </a>

        <nav>
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#about">About</a>
        </nav>

        <div className="home-nav-actions">
          <button
            className="home-login"
            onClick={() => onNavigate?.("login")}
          >
            Login
          </button>
          <button
            className="home-register"
            onClick={() => onNavigate?.("register")}
          >
            Get Started
          </button>
        </div>
      </header>

      <main>
        <section className="home-hero" id="home">
          <div className="home-hero-content">
            <span className="home-eyebrow">
              SMARTER GOVERNMENT SERVICES
            </span>

            <h1>
              Your Voice.
              <br />
              Your Community.
              <br />
              <span>Our Responsibility.</span>
            </h1>

            <p>
              Report public issues, track complaint progress, and
              help build safer, cleaner, better-connected communities
              with CivicResolve AI.
            </p>

            <div className="home-hero-actions">
              <button
                className="home-register"
                onClick={() => onNavigate?.("register")}
              >
                Report an Issue →
              </button>

              <button
                className="home-outline"
                onClick={() => onNavigate?.("login")}
              >
                Track Your Complaint
              </button>
            </div>

            <div className="home-trust">
              <span>✓ Easy reporting</span>
              <span>✓ Status tracking</span>
              <span>✓ AI-assisted prioritization</span>
            </div>
          </div>

          <div className="home-visual">
            <div className="home-visual-icon">🏙️</div>
            <div className="home-floating-card">
              <span className="home-status-dot" />
              <div>
                <strong>Community response</strong>
                <p>Report, track, and stay informed.</p>
              </div>
            </div>
            <div className="home-visual-caption">
              <strong>Better cities start with you.</strong>
              <p>Every report can make a difference.</p>
            </div>
          </div>
        </section>

        <section className="home-features" id="features">
          <div className="home-section-heading">
            <span className="home-eyebrow">WHAT YOU CAN DO</span>
            <h2>One platform. Better public services.</h2>
            <p>
              A simple way to report problems and follow their progress.
            </p>
          </div>

          <div className="home-feature-grid">
            <article className="home-feature-card">
              <div className="home-feature-icon">📢</div>
              <h3>Report Issues</h3>
              <p>
                Submit concerns about roads, waste, water, drainage,
                and electrical safety.
              </p>
            </article>

            <article className="home-feature-card">
              <div className="home-feature-icon">📍</div>
              <h3>Location Mapping</h3>
              <p>
                Use map-based location information to help identify
                where a public issue needs attention.
              </p>
            </article>

            <article className="home-feature-card">
              <div className="home-feature-icon">🤖</div>
              <h3>AI Prioritization</h3>
              <p>
                Assist complaint triage by highlighting issues that
                may need earlier review.
              </p>
            </article>

            <article className="home-feature-card">
              <div className="home-feature-icon">📊</div>
              <h3>Track Progress</h3>
              <p>
                Follow complaint updates and view progress through
                the available tracking features.
              </p>
            </article>
          </div>
        </section>

        <section className="home-about" id="about">
          <div>
            <span className="home-eyebrow">ABOUT CIVICRESOLVE AI</span>
            <h2>Technology for a better community.</h2>
          </div>
          <p>
            CivicResolve AI is designed to bring citizens and public
            service teams together. It combines complaint reporting,
            location information, and AI-assisted prioritization in
            one accessible platform.
          </p>
          <button
            className="home-register"
            onClick={() => onNavigate?.("register")}
          >
            Join the Platform →
          </button>
        </section>
      </main>

      <footer className="home-footer">
        <strong>CivicResolve AI</strong>
        <span>Building better communities, one report at a time.</span>
      </footer>
    </div>
  );
}
