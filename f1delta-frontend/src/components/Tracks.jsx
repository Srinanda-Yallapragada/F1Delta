import { useState, useEffect } from "react";
import "./Tracks.css";

function Tracks() {
  const [trackInfo, setTrackInfo] = useState([]);

  useEffect(() => {
    fetch("/trackInfo")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setTrackInfo(data);
        }
      })
      .catch((err) => {
        console.error("Failed to fetch track info:", err);
      });
  }, []);
  if (trackInfo.length === 0) return null;

  const tracks2024 = trackInfo.filter((track) => track.year === 2024);
  const tracks2025 = trackInfo.filter((track) => track.year === 2025);

  return (
    <div className="tracks-container">
      <div className="track-list">
        <div className="track-year">
          <h2>2024 Tracks</h2>
          {tracks2024.map((track) => (
            <div key={track.meeting_key} className="track-card">
              <h3>{track.meeting_official_name}</h3>
              <p>
                <strong>Location:</strong> {track.location},{" "}
                {track.country_name}
              </p>
              <p>
                <strong>Start Date:</strong>{" "}
                {new Date(track.date_start).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>

        <div className="track-year">
          <h2>2025 Tracks</h2>
          {tracks2025.map((track) => (
            <div key={track.meeting_key} className="track-card">
              <h3>{track.meeting_official_name}</h3>
              <p>
                <strong>Location:</strong> {track.location},{" "}
                {track.country_name}
              </p>
              <p>
                <strong>Start Date:</strong>{" "}
                {new Date(track.date_start).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Tracks;
