import React, { useState } from "react";
import UploadCSV from "./components/UploadCSV";
import DatasetTable from "./components/DatasetTable";
import DatasetCharts from "./components/DatasetCharts";

function App() {
  const [datasetId, setDatasetId] = useState(null);

  return (
    <div>
      <h1>Chemical Equipment Visualizer</h1>
      <UploadCSV onUploadSuccess={(id) => setDatasetId(id)} />
      {datasetId && <DatasetTable datasetId={datasetId} />}
      {datasetId && <DatasetCharts datasetId={datasetId} />}
    </div>
  );
}

export default App;
