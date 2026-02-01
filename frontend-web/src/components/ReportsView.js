import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { Bar, Pie } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from "chart.js";
import config from "../config";
import "../App.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const ReportsView = ({ datasetId, user, authHeader }) => {
    const [chartData, setChartData] = useState([]);
    const [datasetInfo, setDatasetInfo] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const reportRef = useRef(null);

    useEffect(() => {
        if (!datasetId) return;

        const fetchData = async () => {
            setIsLoading(true);
            try {
                // Raw data
                const dataRes = await axios.get(`${config.API_BASE_URL}/dataset/${datasetId}/data/`, {
                    headers: { Authorization: authHeader }
                });
                setChartData(dataRes.data.data);

                // Summary for dataset name
                const summaryRes = await axios.get(`${config.API_BASE_URL}/dataset/${datasetId}/summary/`, {
                    headers: { Authorization: authHeader }
                });
                setDatasetInfo(summaryRes.data);

                setError("");
            } catch (err) {
                console.error("Error fetching report data:", err);
                setError("Failed to load report data.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [datasetId]);

    const handleDownloadPDF = async () => {
        const element = reportRef.current;
        if (!element) return;

        try {
            const canvas = await html2canvas(element, {
                scale: 2,
                useCORS: true,
                logging: true,
            });
            const imgData = canvas.toDataURL("image/png");


            const pdf = new jsPDF("p", "mm", "a4");
            const imgWidth = 210;
            const pageHeight = 297;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            let heightLeft = imgHeight;
            let position = 0;

            pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;

            while (heightLeft >= 0) {
                position = heightLeft - imgHeight;
                pdf.addPage();
                pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
            }

            pdf.save(`Report_${datasetId || "analysis"}.pdf`);
        } catch (err) {
            console.error("PDF generation failed:", err);
            alert("Failed to generate PDF. Please try again.");
        }
    };

    if (isLoading) return <div className="loading-message">Generating Report Preview...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!chartData || chartData.length === 0) return <div className="empty-message">No data available for report.</div>;

    //  Analytics Calculation 
    const flows = chartData.map(d => d.Flowrate);
    const pressures = chartData.map(d => d.Pressure);
    const temps = chartData.map(d => d.Temperature);
    const equipmentNames = chartData.map(d => d["Equipment Name"]);

    const avg = (arr) => (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2);
    const min = (arr) => Math.min(...arr).toFixed(2);
    const max = (arr) => Math.max(...arr).toFixed(2);

    const stats = {
        avgFlow: avg(flows),
        minFlow: min(flows),
        maxFlow: max(flows),
        avgPressure: avg(pressures),
        avgTemp: avg(temps),
        totalRecords: chartData.length,
        uniqueTypes: new Set(chartData.map(d => d.Type)).size
    };

    const typeCounts = {};
    chartData.forEach(d => { typeCounts[d.Type] = (typeCounts[d.Type] || 0) + 1; });

    // Chart Data 
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { ticks: { color: "#333", font: { size: 8 } }, grid: { display: false } },
            y: { ticks: { color: "#333", font: { size: 8 } } }
        }
    };

    const pieOptions = {
        responsive: true,
        plugins: { legend: { position: 'right', labels: { color: "#333", font: { size: 10 } } } }
    };

    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "20px", paddingBottom: "50px" }}>
            <button className="btn-primary" onClick={handleDownloadPDF} style={{ alignSelf: "flex-end", marginRight: "20px" }}>
                Download PDF Report
            </button>

            <div ref={reportRef} style={{
                width: "210mm",
                minHeight: "297mm",
                backgroundColor: "#ffffff",
                color: "#1f2937",
                padding: "20mm",
                boxShadow: "0 0 10px rgba(0,0,0,0.5)",
                fontFamily: "Times New Roman, serif",
                display: "flex",
                flexDirection: "column",
                gap: "20px"
            }}>

                <div style={{ borderBottom: "2px solid #333", paddingBottom: "10px", marginBottom: "10px" }}>
                    <h1 style={{ fontSize: "24pt", margin: "0 0 10px 0", color: "#111827" }}>Chemical Equipment Parameter Visualizer</h1>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11pt" }}>
                        <div>

                            <p style={{ margin: "2px 0" }}><strong>Date:</strong> {new Date().toLocaleString()}</p>
                        </div>
                        <div style={{ textAlign: "right" }}>
                            <p style={{ margin: "2px 0" }}><strong>Generated by:</strong> {user ? user.username : "Unknown"}</p>
                        </div>
                    </div>
                </div>


                <section>
                    <h2 style={{ fontSize: "16pt", borderBottom: "1px solid #ccc", paddingBottom: "5px", marginBottom: "15px", color: "#000000" }}>Dataset Overview Summary</h2>

                    <p style={{ fontSize: "11pt", marginBottom: "20px", lineHeight: "1.6" }}>
                        This report provides an analysis of <strong>{stats.totalRecords}</strong> equipment records, covering <strong>{stats.uniqueTypes}</strong> distinct equipment types.
                        The dataset reveals an average flowrate of <strong>{stats.avgFlow} m³/h</strong>, an average pressure of <strong>{stats.avgPressure} PSI</strong>,
                        and an average operating temperature of <strong>{stats.avgTemp} °C</strong>.
                    </p>

                    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11pt", marginBottom: "10px" }}>
                        <tbody>
                            <tr style={{ backgroundColor: "#f3f4f6" }}>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}><strong>Total Records</strong></td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}>{stats.totalRecords}</td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}><strong>Average Flowrate</strong></td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}>{stats.avgFlow} m³/h</td>
                            </tr>
                            <tr>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}><strong>Unique Types</strong></td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}>{stats.uniqueTypes}</td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}><strong>Average Pressure</strong></td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}>{stats.avgPressure} PSI</td>
                            </tr>
                            <tr style={{ backgroundColor: "#f3f4f6" }}>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }} colSpan="2"></td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}><strong>Average Temperature</strong></td>
                                <td style={{ padding: "8px", border: "1px solid #d1d5db" }}>{stats.avgTemp} °C</td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                <section style={{ breakInside: "avoid" }}>
                    <h2 style={{ fontSize: "16pt", borderBottom: "1px solid #ccc", paddingBottom: "5px", marginBottom: "10px", color: "#000000" }}>Equipment Type Distribution</h2>
                    <div style={{ height: "250px", width: "100%", display: "flex", justifyContent: "center" }}>
                        <Pie data={{
                            labels: Object.keys(typeCounts),
                            datasets: [{
                                data: Object.values(typeCounts),
                                backgroundColor: ["#3b82f6", "#ef4444", "#f59e0b", "#10b981", "#8b5cf6", "#ec4899"],
                            }]
                        }} options={pieOptions} />
                    </div>
                    <p style={{ textAlign: "center", fontStyle: "italic", fontSize: "10pt", marginTop: "5px" }}>Figure 1: Distribution of equipment types in the dataset.</p>
                </section>


                <section>
                    <h2 style={{ fontSize: "16pt", borderBottom: "1px solid #ccc", paddingBottom: "5px", marginBottom: "15px", color: "#000000" }}>Parameter Analysis</h2>

                    <div style={{ marginBottom: "20px", breakInside: "avoid" }}>
                        <h3 style={{ fontSize: "13pt", margin: "0 0 5px 0", color: "#000000" }}>Flowrate Analysis</h3>
                        <div style={{ fontSize: "10pt", marginBottom: "5px" }}>
                            Min: <strong>{stats.minFlow}</strong> | Max: <strong>{stats.maxFlow}</strong> | Avg: <strong>{stats.avgFlow}</strong>
                        </div>
                        <div style={{ height: "180px" }}>
                            <Bar data={{
                                labels: equipmentNames,
                                datasets: [{ label: "Flowrate", data: flows, backgroundColor: "rgba(59, 130, 246, 0.7)" }]
                            }} options={chartOptions} />
                        </div>
                    </div>

                    <div style={{ marginBottom: "20px", breakInside: "avoid" }}>
                        <h3 style={{ fontSize: "13pt", margin: "0 0 5px 0", color: "#000000" }}>Pressure Analysis</h3>
                        <div style={{ fontSize: "10pt", marginBottom: "5px" }}>
                            Avg: <strong>{stats.avgPressure}</strong>
                        </div>
                        <div style={{ height: "180px" }}>
                            <Bar data={{
                                labels: equipmentNames,
                                datasets: [{ label: "Pressure", data: pressures, backgroundColor: "rgba(139, 92, 246, 0.7)" }]
                            }} options={chartOptions} />
                        </div>
                    </div>

                    <div style={{ marginBottom: "20px", breakInside: "avoid" }}>
                        <h3 style={{ fontSize: "13pt", margin: "0 0 5px 0", color: "#000000" }}>Temperature Analysis</h3>
                        <div style={{ fontSize: "10pt", marginBottom: "5px" }}>
                            Avg: <strong>{stats.avgTemp}</strong>
                        </div>
                        <div style={{ height: "180px" }}>
                            <Bar data={{
                                labels: equipmentNames,
                                datasets: [{ label: "Temperature", data: temps, backgroundColor: "rgba(239, 68, 68, 0.7)" }]
                            }} options={chartOptions} />
                        </div>
                    </div>
                </section>


                <section style={{ breakInside: "avoid" }}>
                    <h2 style={{ fontSize: "16pt", borderBottom: "1px solid #ccc", paddingBottom: "5px", marginBottom: "10px", color: "#000000" }}>Full Dataset Data Table</h2>
                    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "10pt" }}>
                        <thead>
                            <tr style={{ backgroundColor: "#374151", color: "#fff" }}>
                                <th style={{ padding: "6px", textAlign: "left" }}>Equipment Name</th>
                                <th style={{ padding: "6px", textAlign: "left" }}>Type</th>
                                <th style={{ padding: "6px", textAlign: "left" }}>Flowrate</th>
                                <th style={{ padding: "6px", textAlign: "left" }}>Pressure</th>
                                <th style={{ padding: "6px", textAlign: "left" }}>Temperature</th>
                            </tr>
                        </thead>
                        <tbody>
                            {chartData.map((row, idx) => (
                                <tr key={idx} style={{ borderBottom: "1px solid #e5e7eb" }}>
                                    <td style={{ padding: "6px" }}>{row["Equipment Name"]}</td>
                                    <td style={{ padding: "6px" }}>{row["Type"]}</td>
                                    <td style={{ padding: "6px" }}>{row["Flowrate"]}</td>
                                    <td style={{ padding: "6px" }}>{row["Pressure"]}</td>
                                    <td style={{ padding: "6px" }}>{row["Temperature"]}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </section>

                <div style={{ marginTop: "auto", borderTop: "1px solid #ccc", paddingTop: "10px", fontSize: "9pt", textAlign: "center", color: "#6b7280" }}>
                    <p>Chemical Equipment Visualizer Report | Page 1</p>
                </div>

            </div>
        </div>
    );
};

export default ReportsView;
