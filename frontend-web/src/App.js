import React, { useState, useEffect } from "react";
import UploadCSV from "./components/UploadCSV";
import DatasetTable from "./components/DatasetTable";
import DatasetCharts from "./components/DatasetCharts";
import DatasetHistory from "./components/DatasetHistory";
import AnalysisSummary from "./components/AnalysisSummary";
import ReportsView from "./components/ReportsView";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import Sidebar from "./components/Sidebar";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState("login");
  const [datasetId, setDatasetId] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [activeTab, setActiveTab] = useState("dashboard");

  useEffect(() => {
    const savedUser = localStorage.getItem("app_user");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      setCurrentPage("dashboard");
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem("app_user", JSON.stringify(userData));
    setCurrentPage("dashboard");
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("app_user");
    setCurrentPage("login");
    setDatasetId(null);
    setActiveTab("dashboard");
  };

  const handleUploadSuccess = (id) => {
    setDatasetId(id);
    setRefreshTrigger(prev => prev + 1);
    setActiveTab('analysis');
  };

  if (!user) {
    if (currentPage === "signup") {
      return <SignupPage onSwitchToLogin={() => setCurrentPage("login")} />;
    }
    return <LoginPage onLogin={handleLogin} onSwitchToSignup={() => setCurrentPage("signup")} />;
  }

  return (
    <div className="app-root">
      <header className="app-header">
        <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
          <img src="/logo.png" alt="Logo" className="header-logo" />
          <h1 className="header-title">Chemical Equipment Parameter Visualizer</h1>
        </div>
        <div className="header-actions">
          <span className="welcome-text">Welcome, <b>{user.username}</b></span>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </header>

      <div className="app-body">
        <Sidebar
          user={user}
          activeTab={activeTab}
          onTabChange={setActiveTab}
          onLogout={handleLogout}
        />

        <main className="main-content">
          {activeTab === 'dashboard' && (
            <div style={{ display: "flex", gap: "20px", width: "100%", maxWidth: "1600px", alignItems: "flex-start", justifyContent: "center", flexWrap: "wrap", margin: "0 auto", paddingTop: "40px" }}>
              <div style={{ display: "flex", flexDirection: "column", gap: "20px", flex: "1", minWidth: "300px", maxWidth: "800px" }}>
                <UploadCSV onUploadSuccess={handleUploadSuccess} authHeader={user.authHeader} />
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <div style={{ width: "100%", maxWidth: "1000px", margin: "0 auto" }}>
              <h2 className="section-title" style={{ color: "#fff", marginBottom: "30px", fontSize: "1.8rem" }}>Upload History</h2>
              <div style={{ background: "#0d1117", padding: "30px", borderRadius: "12px", border: "1px solid rgba(255,255,255,0.1)" }}>
                <DatasetHistory
                  onSelectDataset={(id) => {
                    setDatasetId(id);
                    setActiveTab('analysis');
                  }}
                  refreshTrigger={refreshTrigger}
                  authHeader={user.authHeader}
                />
              </div>
            </div>
          )}

          {activeTab === 'analysis' && (
            <div style={{ width: "100%", maxWidth: "1600px", margin: "0 auto", display: "flex", flexDirection: "column", alignItems: "center" }}>
              {!datasetId ? (
                <div className="empty-message">Please select or upload a dataset first.</div>
              ) : (
                <>
                  <div style={{ width: "100%", marginBottom: "30px" }}>
                    <AnalysisSummary datasetId={datasetId} authHeader={user.authHeader} />
                    <DatasetTable datasetId={datasetId} authHeader={user.authHeader} />
                  </div>
                  <button
                    className="btn-primary"
                    onClick={() => setActiveTab('charts')}
                    style={{ padding: "12px 30px", fontSize: "1.1rem" }}
                  >
                    Show Charts 📊
                  </button>
                </>
              )}
            </div>
          )}

          {activeTab === 'charts' && (
            <div style={{ width: "100%", maxWidth: "100%", margin: "0 auto" }}>
              {!datasetId ? (
                <div className="empty-message">Please select or upload a dataset first.</div>
              ) : (
                <DatasetCharts datasetId={datasetId} authHeader={user.authHeader} />
              )}
            </div>
          )}

          {activeTab === 'reports' && (
            <div style={{ width: "100%", maxWidth: "100%", margin: "0 auto", display: "flex", justifyContent: "center" }}>
              {!datasetId ? (
                <div className="empty-message">Please select or upload a dataset first.</div>
              ) : (
                <ReportsView datasetId={datasetId} user={user} authHeader={user.authHeader} />
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
