import React, { useEffect, useState } from "react";
import axios from "axios";
import config from "../config";
import "../App.css";

const AnalysisSummary = ({ datasetId, authHeader }) => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!datasetId) return;

        const fetchSummary = async () => {
            try {
                const res = await axios.get(`${config.API_BASE_URL}/dataset/${datasetId}/summary/`, {
                    headers: { Authorization: authHeader }
                });
                setSummary(res.data.analytics);
            } catch (error) {
                console.error("Error fetching summary:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchSummary();
    }, [datasetId, authHeader]);

    if (loading) return <div className="loading-text">Calculating metrics...</div>;
    if (!summary) return null;

    return (
        <div className="analysis-summary-container">
            <h2 className="section-title">Analysis Results</h2>


            <div className="summary-cards-grid">
                <div className="summary-card">
                    <div className="card-label">Total Equipment</div>
                    <div className="card-value">{summary.total_count}</div>
                </div>

                <div className="summary-card">
                    <div className="card-label">Avg Flowrate (L/min)</div>
                    <div className="card-value">{summary.avg_flowrate}</div>
                </div>

                <div className="summary-card">
                    <div className="card-label">Avg Pressure (PSI)</div>
                    <div className="card-value">{summary.avg_pressure}</div>
                </div>

                <div className="summary-card">
                    <div className="card-label">Critical Alerts</div>
                    <div className="card-value red-text">{summary.critical_alerts}</div>
                </div>
            </div>


            <div className="text-summary-section">
                <h3>Executive Summary</h3>
                <p>
                    The dataset contains <strong>{summary.total_count} equipment records</strong>.
                    The average flowrate across the system is <strong>{summary.avg_flowrate} L/min</strong>,
                    while the pressure averages at <strong>{summary.avg_pressure} PSI</strong>.
                    System diagnostics successfully identified <strong>{summary.critical_alerts} critical alerts</strong> requiring immediate attention.
                </p>
                <p>
                    <strong>Distribution:</strong> The equipment breakdown consists of
                    {Object.entries(summary.equipment_count_by_type).map(([type, count]) => ` ${type} (${count})`).join(", ")}.
                </p>
            </div>
        </div>
    );
};

export default AnalysisSummary;
