import React, { useState } from "react";
import axios from "axios";
import config from "../config";
import "../App.css";

const SignupPage = ({ onSwitchToLogin }) => {
    const [fullName, setFullName] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        try {
            const res = await axios.post(`${config.API_BASE_URL}/signup/`, {
                username,
                password,
                full_name: fullName
            });
            if (res.status === 201) {
                setSuccess("Account created! Redirecting...");
                setTimeout(onSwitchToLogin, 1500);
            }
        } catch (err) {
            setError(err.response?.data?.error || "Signup failed");
        }
    };

    return (
        <div className="auth-gradient-bg">
            <div className="auth-container">
                <div style={{ display: "flex", justifyContent: "center", marginBottom: "1rem" }}>
                    <img src="/logo.png" alt="Logo" style={{ height: "50px" }} />
                </div>
                <h2 className="auth-title">Create Account</h2>
                <p className="auth-subtitle">Get started with your free account today</p>

                <form onSubmit={handleSubmit}>
                    <div>
                        <label className="auth-label">Full Name</label>
                        <input
                            type="text"
                            placeholder="John Doe"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className="auth-input"
                        />
                    </div>
                    <div>
                        <label className="auth-label">Username</label>
                        <input
                            type="text"
                            placeholder="Choose a username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="auth-input"
                        />
                    </div>

                    <div style={{ display: "flex", gap: "10px" }}>
                        <div style={{ flex: 1 }}>
                            <label className="auth-label">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="auth-input"
                            />
                        </div>
                        <div style={{ flex: 1 }}>
                            <label className="auth-label">Confirm</label>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="auth-input"
                            />
                        </div>
                    </div>


                    {error && <p style={{ color: "#ff7b72", textAlign: "center", fontSize: "0.9rem" }}>{error}</p>}
                    {success && <p style={{ color: "#00e676", textAlign: "center", fontSize: "0.9rem" }}>{success}</p>}

                    <button type="submit" className="auth-btn">
                        Create Account
                    </button>

                    <p style={{ textAlign: "center", marginTop: "20px", color: "#8b949e", fontSize: "0.9rem" }}>
                        Already have an account? <span onClick={onSwitchToLogin} className="auth-link" style={{ color: "#ffffff", fontWeight: "bold" }}>Sign in</span>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default SignupPage;
