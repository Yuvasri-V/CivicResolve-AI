
import { useState } from "react";
import "./AdminDashboardPage.css";

export default function AdminDashboardPage({ onNavigate }) {
  const [section, setSection] = useState("overview");

  const menu = [
    { id: "overview", label: "Overview", icon: "▦" },
    { id: "complaints", label: "Manage Complaints", icon: "☷" },
    { id: "analytics", label: "Analytics", icon: "▥" },
    { id: "map", label: "Complaint Map", icon: "⌖" },
  ];

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <h2>CR <span>Admin Panel</span></h2>
        <p className="admin-menu-title">WORKSPACE</p>

        {menu.map((item) => (
          <button
            key={item.id}
            className={section === item.id ? "admin-menu active" : "admin-menu"}
            onClick={() => {
              setSection(item.id);
              if (item.id === "complaints") onNavigate?.("admin");
            }}
          >
            <span>{item.icon}</span> {item.label}
          </button>
        ))}

        <div className="admin-sidebar-bottom">
          <button onClick={() => onNavigate?.("home")}>← Home</button>
          <button onClick={() => onNavigate?.("login")}>Sign Out</button>
        </div>
      </aside>

      <main className="admin-main">
        <header className="admin-header">
          <div>
            <h1>Admin Dashboard</h1>
            <p>Monitor and manage public grievances.</p>
          </div>
          <span className="admin-badge">Administrator</span>
        </header>

        <section className="admin-welcome">
          <div>
            <span>GRIEVANCE MANAGEMENT</span>
            <h2>Welcome to your workspace</h2>
            <p>
              Review reported issues, monitor priority levels, and
              coordinate responses with service teams.
            </p>
          </div>
          <div className="admin-illustration">🏢</div>
        </section>

        <section className="admin-stat-grid">
          <article className="admin-stat">
            <span>📋</span>
            <p>Total Complaints</p>
            <strong>—</strong>
            <small>Connect existing complaint data</small>
          </article>
          <article className="admin-stat">
            <span>⏳</span>
            <p>Pending Review</p>
            <strong>—</strong>
            <small>Based on actual complaint status</small>
          </article>
          <article className="admin-stat">
            <span>🚨</span>
            <p>High Priority</p>
            <strong>—</strong>
            <small>Based on existing priority results</small>
          </article>
          <article className="admin-stat">
            <span>✓</span>
            <p>Resolved</p>
            <strong>—</strong>
            <small>Based on resolved complaints</small>
          </article>
        </section>

        <section className="admin-workspace">
          <h2>
            {menu.find((item) => item.id === section)?.label}
          </h2>

          {section === "overview" && (
            <div className="admin-empty">
              <span>📊</span>
              <h3>Complaint Overview</h3>
              <p>
                Your existing backend data will be connected here
                without creating new API endpoints.
              </p>
              <button onClick={() => setSection("complaints")}>
                View Complaint Management
              </button>
            </div>
          )}

          {section === "complaints" && (
            <div className="admin-empty">
              <span>🗂️</span>
              <h3>Complaint Management</h3>
              <p>
                Use your existing complaint-management component
                to view and update real complaints.
              </p>
              <button onClick={() => onNavigate?.("admin")}>
                Open Existing Admin Dashboard
              </button>
            </div>
          )}

          {section === "analytics" && (
            <div className="admin-empty">
              <span>📈</span>
              <h3>Analytics</h3>
              <p>
                Connect the existing dashboard charts and priority
                summaries to display actual results.
              </p>
            </div>
          )}

          {section === "map" && (
            <div className="admin-empty">
              <span>📍</span>
              <h3>Complaint Map</h3>
              <p>
                Open your existing complaints map to inspect
                reported issue locations.
              </p>
              <button onClick={() => onNavigate?.("admin")}>
                Open Existing Admin Dashboard
              </button>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
