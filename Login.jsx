
import { useState } from "react";
import "./AuthPages.css";

export default function Login({ onLogin, onNavigate }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("citizen");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    setError("");

    if (!email.trim() || !password.trim()) {
      setError("Please enter your email and password.");
      return;
    }

    // Frontend demo only. This does not authenticate an account.
    if (onLogin) {
      onLogin({ email, role });
    } else {
      setError("Login navigation is not connected yet.");
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-brand">
        <div className="brand-mark">CR</div>
        <h1>CivicResolve AI</h1>
        <p>
          Making communities better through smarter public
          grievance management.
        </p>
        <div className="brand-feature">
          <span>✓</span> Report public issues
        </div>
        <div className="brand-feature">
          <span>✓</span> Track complaint status
        </div>
        <div className="brand-feature">
          <span>✓</span> Support faster responses
        </div>
      </section>

      <section className="auth-card">
        <button
          className="back-home"
          type="button"
          onClick={() => onNavigate?.("home")}
        >
          ← Back to Home
        </button>

        <h2>Welcome back!</h2>
        <p className="auth-subtitle">
          Sign in to continue to CivicResolve AI.
        </p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="login-role">Login as</label>
          <select
            id="login-role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="citizen">Citizen</option>
            <option value="admin">Administrator (demo)</option>
          </select>

          <label htmlFor="login-email">Email address</label>
          <input
            id="login-email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="login-password">Password</label>
          <div className="password-field">
            <input
              id="login-password"
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              className="show-password"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button className="auth-submit" type="submit">
            Sign In
          </button>
        </form>

        <p className="auth-switch">
          New to CivicResolve?{" "}
          <button
            type="button"
            onClick={() => onNavigate?.("register")}
          >
            Create an account
          </button>
        </p>
      </section>
    </main>
  );
}
