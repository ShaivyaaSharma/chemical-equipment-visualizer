import React, { useState } from "react";
import axios from "axios";

// Component for uploading CSV files
const UploadCSV = ({ onUploadSuccess, authHeader }) => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage("Please select a file first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await axios.post("http://127.0.0.1:8000/api/upload-csv/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    "Authorization": authHeader
                },
            });

            setMessage(res.data.message);
            if (onUploadSuccess) onUploadSuccess(res.data.dataset_id);
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data) {

                const errorMsg = err.response.data.error || err.response.data.detail || err.response.data.message || "Upload failed.";
                setMessage(errorMsg);
            } else {
                setMessage("Upload failed. Please check server connection.");
            }
        }
    };

    return (
        <div className="upload-container">
            <h2 className="section-title-upload">Upload Dataset</h2>

            <div className="upload-dropzone" onClick={() => document.getElementById('fileInput').click()}>
                <input
                    id="fileInput"
                    type="file"
                    accept=".csv,.xlsx"
                    onChange={handleFileChange}
                    style={{ display: "none" }}
                />

                <div className="upload-icon-wrapper">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="#8b949e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M17 8L12 3L7 8" stroke="#8b949e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M12 3V15" stroke="#8b949e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>

                <p className="upload-text-main">
                    Click to upload CSV
                </p>
                <p className="upload-text-sub">
                    or drag and drop file here
                </p>
                <p className="upload-text-limit">
                    Supports .csv, .xlsx (Max 50MB)
                </p>

                {file && (
                    <div className="selected-file-pill">
                        Selected: {file.name}
                    </div>
                )}
            </div>

            {file && (
                <button className="btn-primary" onClick={handleUpload} style={{ width: "100%", marginTop: "20px" }}>
                    Upload & Visualize
                </button>
            )}

            {message && (
                <p style={{
                    marginTop: "15px",
                    color: message.includes("success") || message.includes("Uploaded") ? "var(--primary-color)" : "#ff7b72"
                }}>
                    {message}
                </p>
            )}
        </div>
    );
};

export default UploadCSV;
