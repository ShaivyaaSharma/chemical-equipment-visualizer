import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar, Line, Pie, Doughnut } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from "chart.js";
import config from "../config";
import "../App.css";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const DatasetCharts = ({ datasetId, authHeader }) => {
    const [chartData, setChartData] = useState([]);
    const [flowChartType, setFlowChartType] = useState('bar');
    const [tempChartType, setTempChartType] = useState('line');
    const [pressureChartType, setPressureChartType] = useState('bar');
    const [distChartType, setDistChartType] = useState('pie');

    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (!datasetId) return;

        const fetchData = async () => {
            setIsLoading(true);
            try {
                const res = await axios.get(`${config.API_BASE_URL}/dataset/${datasetId}/data/`, {
                    headers: { Authorization: authHeader }
                });
                setChartData(res.data.data);
                setErrorMessage("");
            } catch (err) {
                console.error("Error fetching chart data:", err);
                setErrorMessage("Unable to load chart data. Please try again later.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [datasetId]);

    if (!datasetId) return null;
    if (errorMessage) return <div className="error-message">{errorMessage}</div>;
    if (isLoading) return <div className="loading-message">Loading visualization...</div>;
    if (chartData.length === 0) return <div className="empty-message">No data available for visualization.</div>;

    const equipmentNames = chartData.map((item) => item["Equipment Name"]);
    const flowRates = chartData.map((item) => item["Flowrate"]);
    const temperatures = chartData.map((item) => item["Temperature"]);
    const pressures = chartData.map((item) => item["Pressure"]);

    const equipmentTypeCounts = {};
    chartData.forEach((item) => {
        const type = item["Type"];
        equipmentTypeCounts[type] = (equipmentTypeCounts[type] || 0) + 1;
    });


    const calculateHistogram = (data, binCount = 10) => {
        if (!data || data.length === 0) return { labels: [], count: [] };
        const min = Math.min(...data);
        const max = Math.max(...data);
        const step = (max - min) / binCount || 10;

        const bins = Array(binCount).fill(0);
        const labels = Array(binCount).fill(0).map((_, i) => {
            const start = (min + i * step).toFixed(1);
            const end = (min + (i + 1) * step).toFixed(1);
            return `${start} - ${end}`;
        });

        data.forEach(val => {
            const index = Math.min(Math.floor((val - min) / step), binCount - 1);
            bins[index]++;
        });

        return { labels, data: bins };
    };

    const flowHistogram = calculateHistogram(flowRates);
    const tempHistogram = calculateHistogram(temperatures);

    const requiredCols = ["Equipment Name", "Flowrate", "Temperature", "Type"];
    const hasRequiredCols = chartData.length > 0 && requiredCols.every(col => Object.keys(chartData[0]).includes(col));

    if (!hasRequiredCols) {
        return (
            <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
                <div className="container-card" style={{ textAlign: "center", color: "var(--text-secondary)" }}>
                    <p>Visualizations unavailable. Missing required columns.</p>
                </div>
            </div>
        );
    }

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: { bottom: 50 }
        },
        plugins: {
            legend: { position: "top", labels: { color: "#c9d1d9" } }
        },
        scales: {
            y: { ticks: { color: "#8b949e" }, grid: { color: "rgba(255,255,255,0.1)" } },
            x: { ticks: { color: "#8b949e" }, grid: { display: false } }
        }
    };

    return (
        <div style={{
            width: "100%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            paddingBottom: "100px"
        }}>
            <div style={{ width: "100%", maxWidth: "1600px", padding: "0 20px", marginBottom: "30px" }}>
                <h2 className="section-title" style={{ margin: 0 }}>Equipment Analytics</h2>
            </div>

            <div style={{
                width: "90%",
                maxWidth: "1200px",
                display: "flex",
                flexDirection: "column",
                gap: "100px",
                padding: "50px 20px"
            }}>

                <div className="chart-wrapper" style={{ height: "500px", padding: "20px", position: "relative" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "15px" }}>
                        <h3 style={{ color: "var(--text-primary)", margin: 0, fontSize: "1.1rem" }}>Flowrate Analysis</h3>
                        <select value={flowChartType} onChange={(e) => setFlowChartType(e.target.value)} className="chart-select" style={{ marginRight: "30px", padding: "6px 10px", cursor: "pointer", borderRadius: "6px", background: "#161b22", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", fontSize: "0.9rem" }}>
                            <option value="bar">Bar Chart</option>
                            <option value="line">Line Chart</option>
                            <option value="histogram">Histogram</option>
                        </select>
                    </div>
                    {flowChartType === 'histogram' ? (
                        <Bar
                            data={{ labels: flowHistogram.labels, datasets: [{ label: "Frequency", data: flowHistogram.data, backgroundColor: "rgba(34, 211, 238, 0.6)", barPercentage: 1.0, categoryPercentage: 1.0 }] }}
                            options={commonOptions}
                        />
                    ) : flowChartType === 'bar' ? (
                        <Bar data={{ labels: equipmentNames, datasets: [{ label: "Flowrate (m³/h)", data: flowRates, backgroundColor: "rgba(34, 211, 238, 0.6)", borderColor: "rgba(34, 211, 238, 1)", borderWidth: 1 }] }} options={commonOptions} />
                    ) : (
                        <Line data={{ labels: equipmentNames, datasets: [{ label: "Flowrate (m³/h)", data: flowRates, borderColor: "rgba(34, 211, 238, 1)", backgroundColor: "rgba(34, 211, 238, 0.2)", tension: 0.4 }] }} options={commonOptions} />
                    )}
                </div>

                <div className="chart-wrapper" style={{ height: "500px", padding: "20px", position: "relative" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "15px" }}>
                        <h3 style={{ color: "var(--text-primary)", margin: 0, fontSize: "1.1rem" }}>Temperature Trends</h3>
                        <select value={tempChartType} onChange={(e) => setTempChartType(e.target.value)} className="chart-select" style={{ marginRight: "30px", padding: "6px 10px", cursor: "pointer", borderRadius: "6px", background: "#161b22", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", fontSize: "0.9rem" }}>
                            <option value="line">Line Chart</option>
                            <option value="bar">Bar Chart</option>
                            <option value="histogram">Histogram</option>
                        </select>
                    </div>
                    {tempChartType === 'histogram' ? (
                        <Bar
                            data={{ labels: tempHistogram.labels, datasets: [{ label: "Frequency", data: tempHistogram.data, backgroundColor: "rgba(248, 113, 113, 0.6)", barPercentage: 1.0, categoryPercentage: 1.0 }] }}
                            options={commonOptions}
                        />
                    ) : tempChartType === 'line' ? (
                        <Line data={{ labels: equipmentNames, datasets: [{ label: "Temperature (°C)", data: temperatures, borderColor: "#f87171", backgroundColor: "rgba(248, 113, 113, 0.2)", tension: 0.3, pointBackgroundColor: "#f87171" }] }} options={commonOptions} />
                    ) : (
                        <Bar data={{ labels: equipmentNames, datasets: [{ label: "Temperature (°C)", data: temperatures, backgroundColor: "rgba(248, 113, 113, 0.6)", borderColor: "#f87171", borderWidth: 1 }] }} options={commonOptions} />
                    )}
                </div>


                <div className="chart-wrapper" style={{ height: "500px", padding: "20px", position: "relative" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "15px" }}>
                        <h3 style={{ color: "var(--text-primary)", margin: 0, fontSize: "1.1rem" }}>Pressure Analysis</h3>
                        <select value={pressureChartType} onChange={(e) => setPressureChartType(e.target.value)} className="chart-select" style={{ marginRight: "30px", padding: "6px 10px", cursor: "pointer", borderRadius: "6px", background: "#161b22", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", fontSize: "0.9rem" }}>
                            <option value="bar">Bar Chart</option>
                            <option value="line">Line Chart</option>
                        </select>
                    </div>
                    {pressureChartType === 'bar' ? (
                        <Bar data={{ labels: equipmentNames, datasets: [{ label: "Pressure (PSI)", data: pressures, backgroundColor: "rgba(167, 139, 250, 0.6)", borderColor: "rgba(167, 139, 250, 1)", borderWidth: 1 }] }} options={commonOptions} />
                    ) : (
                        <Line data={{ labels: equipmentNames, datasets: [{ label: "Pressure (PSI)", data: pressures, borderColor: "rgba(167, 139, 250, 1)", backgroundColor: "rgba(167, 139, 250, 0.2)", tension: 0.4 }] }} options={commonOptions} />
                    )}
                </div>

                <div className="chart-wrapper" style={{ height: "500px", padding: "20px", display: "flex", flexDirection: "column", position: "relative" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "15px" }}>
                        <h3 style={{ color: "var(--text-primary)", margin: 0, fontSize: "1.1rem" }}>Equipment Type</h3>
                        <select value={distChartType} onChange={(e) => setDistChartType(e.target.value)} className="chart-select" style={{ marginRight: "30px", padding: "6px 10px", cursor: "pointer", borderRadius: "6px", background: "#161b22", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", fontSize: "0.9rem" }}>
                            <option value="pie">Pie Chart</option>
                            <option value="doughnut">Doughnut Chart</option>
                            <option value="bar">Bar Chart</option>
                        </select>
                    </div>
                    <div style={{ flex: 1, position: "relative", width: "100%", height: "100%" }}>
                        {distChartType === 'pie' && <Pie data={{ labels: Object.keys(equipmentTypeCounts), datasets: [{ data: Object.values(equipmentTypeCounts), backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"], borderWidth: 0 }] }} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "right", labels: { color: "#c9d1d9", padding: 10, font: { size: 11 } } } } }} />}
                        {distChartType === 'doughnut' && <Doughnut data={{ labels: Object.keys(equipmentTypeCounts), datasets: [{ data: Object.values(equipmentTypeCounts), backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"], borderWidth: 0 }] }} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "right", labels: { color: "#c9d1d9", padding: 10, font: { size: 11 } } } } }} />}
                        {distChartType === 'bar' && <Bar data={{ labels: Object.keys(equipmentTypeCounts), datasets: [{ label: 'Count', data: Object.values(equipmentTypeCounts), backgroundColor: "#36A2EB" }] }} options={commonOptions} />}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default DatasetCharts;
