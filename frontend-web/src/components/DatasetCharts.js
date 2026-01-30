import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar, Line, Pie } from "react-chartjs-2";
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

const DatasetCharts = ({ datasetId }) => {
    const [chartData, setChartData] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (!datasetId) return;

        const fetchData = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get(`${config.API_BASE_URL}/dataset/${datasetId}/data/`);
                setChartData(response.data.data);
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

    const equipmentTypeCounts = {};
    chartData.forEach((item) => {
        const type = item["Type"];
        equipmentTypeCounts[type] = (equipmentTypeCounts[type] || 0) + 1;
    });

    return (
        <div className="charts-container">
            <h2 className="section-title">Equipment Analytics</h2>

            <div className="chart-wrapper">
                <h3>Flowrate Analysis</h3>
                <Bar
                    data={{
                        labels: equipmentNames,
                        datasets: [
                            {
                                label: "Flowrate (m³/h)",
                                data: flowRates,
                                backgroundColor: "rgba(75, 192, 192, 0.6)",
                                borderColor: "rgba(75, 192, 192, 1)",
                                borderWidth: 1,
                            },
                        ],
                    }}
                    options={{
                        responsive: true,
                        plugins: {
                            legend: { position: "top" },
                            title: { display: false }
                        }
                    }}
                />
            </div>

            <div className="chart-wrapper">
                <h3>Temperature Trends</h3>
                <Line
                    data={{
                        labels: equipmentNames,
                        datasets: [
                            {
                                label: "Temperature (°C)",
                                data: temperatures,
                                borderColor: "rgba(255, 99, 132, 0.8)",
                                backgroundColor: "rgba(255, 99, 132, 0.3)",
                                tension: 0.3,
                            },
                        ],
                    }}
                    options={{
                        responsive: true,
                        plugins: { legend: { position: "top" } }
                    }}
                />
            </div>

            <div className="chart-wrapper pie-chart">
                <h3>Equipment Distribution</h3>
                <Pie
                    data={{
                        labels: Object.keys(equipmentTypeCounts),
                        datasets: [
                            {
                                data: Object.values(equipmentTypeCounts),
                                backgroundColor: [
                                    "#36A2EB",
                                    "#FF6384",
                                    "#FFCE56",
                                    "#4BC0C0",
                                    "#9966FF",
                                    "#FF9F40",
                                ],
                            },
                        ],
                    }}
                    options={{
                        responsive: true,
                        plugins: { legend: { position: "right" } }
                    }}
                />
            </div>
        </div>
    );
};

export default DatasetCharts;
