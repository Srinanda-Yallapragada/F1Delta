import { useState } from "react";
import "./App.css";
import DriverBasicStats from "./components/driverBasicStats.jsx";
import Tracks from "./components/Tracks.jsx";

function App() {
  const [selectedDriver, setSelectedDriver] = useState(1);

  const driverNumbers = [1, 4, 10, 14, 16, 18, 22, 23, 27, 31, 44, 55, 63, 81];

  const handleDriverChange = (event) => {
    setSelectedDriver(Number(event.target.value));
  };

  return (
    <div className="driver-info">
      <h1>F1 Driver Information</h1>

      <div className="driver-selector">
        <label htmlFor="driver-select">Select Driver Number:</label>
        <select
          id="driver-select"
          value={selectedDriver}
          onChange={handleDriverChange}
        >
          {driverNumbers.map((number) => (
            <option key={number} value={number}>
              {number}
            </option>
          ))}
        </select>
      </div>

      <DriverBasicStats driverNumber={selectedDriver} />
      <Tracks driverNumber={selectedDriver} />
    </div>
  );
}

export default App;
