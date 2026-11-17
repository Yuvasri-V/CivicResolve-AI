
import { useState } from "react";
import "./AuthPages.css";

export default function Register({ onNavigate }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    setMessage("");

    if (password.length < 8) {
      setMessage("Password must contain at least 8 characters.");
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Passwords do not match.");
      return;
    }

    setMessage(
      "Form validation successful. Account creation needs a registration API."
    );
  }

  return (
    <main className="auth-page">
      <section className="auth-brand">
        <div className="brand-mark">CR</div>
        <h1>Join CivicResolve AI</h1>
        <p>
          Help your community by reporting issues and tracking
          their progress.
        </p>
        <div className="brand-feature">
          <span>✓</span> Easy complaint reporting
        </div>
        <div className="brand-feature">
          <span>✓</span> Complaint status tracking
        </div>
        <div className="brand-feature">
          <span>✓</span> Community-focused services
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

        <h2>Create your account</h2>
        <p className="auth-subtitle">
          Enter your details to get started.
        </p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="register-name">Full name</label>
          <input
            id="register-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your full name"
            required
          />

          <label htmlFor="register-email">Email address</label>
          <input
            id="register-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />

          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 8 characters"
            minLength={8}
            required
          />

          <label htmlFor="register-confirm">Confirm password</label>
          <input
            id="register-confirm"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Enter password again"
            required
          />

          {message && (
            <p className="auth-message">{message}</p>
          )}

          <button className="auth-submit" type="submit">
            Create Account
          </button>
        </form>

        <p className="auth-switch">
          Already registered?{" "}
          <button
            type="button"
            onClick={() => onNavigate?.("login")}
          >
            Sign in
          </button>
        </p>
      </section>
    </main>
  );
}
