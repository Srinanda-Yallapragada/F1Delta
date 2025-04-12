import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';

function TrackGeojson({ trackId }) {
  const [geojson, setGeojson] = useState(null);
  const [error, setError] = useState(null);
  const svgRef = useRef();
  const width = 200; // Adjust width as needed
  const height = 150; // Adjust height as needed

  useEffect(() => {
    if (!trackId) {
      return; // Don't fetch if no trackId is provided
    }

    fetch(`/f1-circuits/circuits/${trackId}.geojson`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => setGeojson(data))
      .catch(error => {
        console.error(`Failed to load GeoJSON for ${trackId}:`, error);
        setError(error.message);
      });
  }, [trackId]); // Re-run effect when trackId changes

  useEffect(() => {
    if (geojson && svgRef.current) {
      const svg = d3.select(svgRef.current)
        .attr("width", width)
        .attr("height", height);

      const projection = d3.geoIdentity()
        .fitSize([width * 0.8, height * 0.8], geojson); // Add some padding

      const path = d3.geoPath().projection(projection);

      svg.selectAll("path")
        .data(geojson.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("fill", "#eee")
        .attr("stroke", "black")
        .attr("stroke-width", 0.5);

      // Optional: Add a title to each map
      svg.append("text")
        .attr("x", width / 2)
        .attr("y", height - 10)
        .attr("text-anchor", "middle")
        .style("font-size", "0.8em")
        .text(trackId);
    }
  }, [geojson, trackId]);

  if (error) {
    return <p className="geojson-error">Error loading map for {trackId}</p>;
  }

  if (!geojson) {
    return <p className="geojson-loading">Loading map for {trackId}...</p>;
  }

  return (
    <div className="track-geojson-container">
      <svg ref={svgRef}></svg>
    </div>
  );
}

export default TrackGeojson;