import React, { useEffect, useState } from "react";
import axios from "axios";
import config from "../config";
import "../App.css";

const DatasetHistory = ({ onSelectDataset, refreshTrigger, authHeader }) => {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        fetchHistory();
    }, [refreshTrigger]);

    const fetchHistory = async () => {
        try {
            const res = await axios.get(`${config.API_BASE_URL}/datasets/`, {
                headers: { Authorization: authHeader }
            });
            setHistory(res.data);
        } catch (err) {
            console.error("Error fetching history:", err);
        }
    };

    return (
        <div className="container-card" style={{ maxWidth: "100%", background: "transparent", border: "none", padding: 0, boxShadow: "none" }}>
            <h3 className="section-title" style={{ fontSize: "1.2rem", marginBottom: "15px", borderLeft: "none", paddingLeft: 0 }}>Recent History</h3>
            {history.length === 0 ? (
                <p className="empty-message">No history yet.</p>
            ) : (
                <ul className="history-list">
                    {history.map((item) => (
                        <li key={item.id} className="history-item">
                            <div className="history-icon-wrapper">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M14 2V8H20" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M8 13H16" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M8 17H16" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M10 9H8" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>

                            <div className="history-content">
                                <div className="history-name">{item.name}</div>
                                <div className="history-meta">
                                    Uploaded {new Date(item.uploaded_at).toLocaleDateString()} • 2.4 MB
                                </div>
                                <p style={{ fontSize: "1rem", color: "#8b949e", marginTop: "8px", lineHeight: "1.4", maxWidth: "90%" }}>
                                    {item.summary}
                                </p>
                            </div>

                            <div className="history-actions">
                                <span className="status-badge">ANALYZED</span>
                                <button className="btn-view" onClick={() => onSelectDataset(item.id)}>View</button>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DatasetHistory;
