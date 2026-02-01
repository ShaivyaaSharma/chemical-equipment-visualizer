import React, { useState } from "react";
import axios from "axios";
import config from "../config";
import "../App.css";

const LoginPage = ({ onLogin, onSwitchToSignup }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post(`${config.API_BASE_URL}/login/`, { username, password });
            if (res.status === 200) {

                const authHeader = "Basic " + btoa(username + ":" + password);
                onLogin({ username, authHeader });
            }
        } catch (err) {
            setError(err.response?.data?.error || "Login failed");
        }
    };

    return (
        <div className="auth-gradient-bg">
            <div className="auth-container">
                <div style={{ display: "flex", justifyContent: "center", marginBottom: "1rem" }}>
                    <img src="/logo.png" alt="Logo" style={{ height: "50px" }} />
                </div>
                <h2 className="auth-title">Welcome back</h2>
                <p className="auth-subtitle">Enter your credentials to access the dashboard</p>

                <form onSubmit={handleSubmit}>
                    <div>
                        <label className="auth-label">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="auth-input"
                        />
                    </div>
                    <div>
                        <div style={{ display: "flex", justifyContent: "space-between" }}>
                            <label className="auth-label">Password</label>
                        </div>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="auth-input"
                        />
                    </div>

                    {error && <p style={{ color: "#ff7b72", textAlign: "center", fontSize: "0.9rem" }}>{error}</p>}

                    <button type="submit" className="auth-btn">
                        Sign In
                    </button>

                    <p style={{ textAlign: "center", marginTop: "20px", color: "#8b949e", fontSize: "0.9rem" }}>
                        Don't have an account? <span onClick={onSwitchToSignup} className="auth-link" style={{ color: "#ffffff", fontWeight: "bold" }}>Sign up</span>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;
