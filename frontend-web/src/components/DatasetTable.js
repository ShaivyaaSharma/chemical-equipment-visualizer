import React, { useEffect, useState } from "react";
import axios from "axios";
import config from "../config";
import "../App.css";

const DatasetTable = ({ datasetId, authHeader }) => {
    const [tableData, setTableData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        if (!datasetId) return;

        const fetchTableData = async () => {
            setIsLoading(true);
            setErrorMessage("");
            try {
                const res = await axios.get(`${config.API_BASE_URL}/dataset/${datasetId}/data/`, {
                    headers: { Authorization: authHeader }
                });
                setTableData(res.data.data);
            } catch (err) {
                console.error("Error fetching table data:", err);
                setErrorMessage("Failed to load dataset. Please check your connection.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchTableData();
    }, [datasetId, authHeader]);

    if (!datasetId) return null;
    if (isLoading) return <div className="loading-message">Loading data...</div>;
    if (errorMessage) return <div className="error-message">{errorMessage}</div>;
    if (tableData.length === 0) return <div className="empty-message">No records found.</div>;

    const columns = Object.keys(tableData[0]);

    return (
        <div className="table-container">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2 className="section-title">Dataset Overview</h2>
                <span style={{ color: "var(--text-secondary)" }}>Total Records: {tableData.length}</span>
            </div>
            <div className="table-responsive">
                <table className="data-table">
                    <thead>
                        <tr>
                            {columns.map((col) => (
                                <th key={col}>{col}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {tableData.map((row, idx) => (
                            <tr key={idx}>
                                {columns.map((col) => (
                                    <td key={col}>{row[col]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DatasetTable;
