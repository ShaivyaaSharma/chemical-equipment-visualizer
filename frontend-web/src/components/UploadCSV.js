import React, { useState } from "react";
import axios from "axios";

// Component for uploading CSV files
const UploadCSV = ({ onUploadSuccess }) => {
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
                headers: { "Content-Type": "multipart/form-data" },
            });

            setMessage(res.data.message);
            if (onUploadSuccess) onUploadSuccess(res.data.dataset_id);
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data.error) {
                setMessage(err.response.data.error);
            } else {
                setMessage("Upload failed.");
            }
        }
    };

    return (
        <div style={{ margin: "20px" }}>
            <h2>Upload CSV</h2>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
                Upload
            </button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default UploadCSV;
