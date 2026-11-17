import "./CitizenDashboard.css";
import { useState } from "react";
import "../App.css";

export default function CitizenDashboard({ onNavigate }) {
  const [activeSection, setActiveSection] = useState("overview");

  const sections = [
    { id: "overview", label: "Overview", icon: "▦" },
    { id: "report", label: "Report an Issue", icon: "＋" },
    { id: "track", label: "Track Complaint", icon: "◎" },
    { id: "community", label: "Community", icon: "♧" },
  ];

  function openSection(id) {
    setActiveSection(id);

    if (id === "report") onNavigate?.("report");
    if (id === "track") onNavigate?.("track");
    if (id === "community") onNavigate?.("community");
  }

  return (
    <div className="citizen-layout">
      <aside className="citizen-sidebar">
        <div className="citizen-brand">
          <span className="citizen-brand-mark">CR</span>
          <span>CivicResolve AI</span>
        </div>

        <p className="citizen-menu-heading">CITIZEN MENU</p>

        {sections.map((section) => (
          <button
            key={section.id}
            className={`citizen-menu-item ${
              activeSection === section.id ? "active" : ""
            }`}
            onClick={() => openSection(section.id)}
          >
            <span>{section.icon}</span>
            {section.label}
          </button>
        ))}

        <div className="citizen-sidebar-bottom">
          <button onClick={() => onNavigate?.("home")}>
            ← Back to Home
          </button>
          <button onClick={() => onNavigate?.("login")}>
            Sign Out
          </button>
        </div>
      </aside>

      <main className="citizen-main">
        <header className="citizen-topbar">
          <div>
            <h1>Citizen Dashboard</h1>
            <p>Welcome! Help make your community better.</p>
          </div>
          <div className="citizen-avatar">C</div>
        </header>

        <section className="citizen-welcome">
          <div>
            <span className="citizen-welcome-label">YOUR COMMUNITY MATTERS</span>
            <h2>Every report makes a difference.</h2>
            <p>
              Report public issues and use the available tools to follow
              their progress.
            </p>
            <button
              className="citizen-primary-button"
              onClick={() => onNavigate?.("report")}
            >
              + Report an Issue
            </button>
          </div>
          <div className="citizen-welcome-art">🏙️</div>
        </section>

        <section className="citizen-stats">
          <article className="citizen-stat-card">
            <span className="citizen-stat-icon">📋</span>
            <p>My Complaints</p>
            <h3>—</h3>
            <small>Connect complaint data to display totals</small>
          </article>

          <article className="citizen-stat-card">
            <span className="citizen-stat-icon">⏳</span>
            <p>In Progress</p>
            <h3>—</h3>
            <small>Based on current complaint statuses</small>
          </article>

          <article className="citizen-stat-card">
            <span className="citizen-stat-icon">✓</span>
            <p>Resolved</p>
            <h3>—</h3>
            <small>Based on resolved complaints</small>
          </article>
        </section>

        <section className="citizen-quick-actions">
          <h2>Quick Actions</h2>
          <div className="citizen-action-grid">
            <button onClick={() => onNavigate?.("report")}>
              <span>📢</span>
              <strong>Report a Problem</strong>
              <small>Submit a new public grievance</small>
            </button>

            <button onClick={() => onNavigate?.("track")}>
              <span>📍</span>
              <strong>Track a Complaint</strong>
              <small>Check your complaint status</small>
            </button>

            <button onClick={() => onNavigate?.("community")}>
              <span>🌱</span>
              <strong>Community Updates</strong>
              <small>Explore community information</small>
            </button>
          </div>
        </section>

        <footer className="citizen-footer">
          CivicResolve AI · Better services through community participation
        </footer>
      </main>
    </div>
  );
}
