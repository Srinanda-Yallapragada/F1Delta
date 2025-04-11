import { useState, useEffect } from "react";
import "./driverBasicStats.css";

function DriverBasicStats({ driverNumber }) {
  const [driverInfo, setDriverInfo] = useState(null);

  useEffect(() => {
    fetch(`/driverInfo?driver_number=${driverNumber}&session_key=latest`)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          setDriverInfo(data[0]);
        }
      });
  }, [driverNumber]);

  if (!driverInfo) return null;

  return (
    <div className="driver-stats-container">
      <div className="driver-card">
        <div
          className="driver-header"
          style={{ backgroundColor: `#${driverInfo.team_colour}` }}
        >
          <div className="driver-number">{driverInfo.driver_number}</div>
          <div className="driver-acronym">{driverInfo.name_acronym}</div>
        </div>

        <div className="driver-content">
          <div className="driver-image">
            <img src={driverInfo.headshot_url} alt={driverInfo.full_name} />
          </div>

          <div className="driver-info">
            <h2>{driverInfo.full_name}</h2>
            <div className="driver-details">
              <p>
                <span>Team:</span> {driverInfo.team_name}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DriverBasicStats;
