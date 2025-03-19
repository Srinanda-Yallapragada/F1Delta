import "./style.css";

import { setupCounter } from "./counter.js";
import * as d3 from "d3";

document.addEventListener("DOMContentLoaded", () => {
  const svg = d3
    .select("#app")
    .append("svg")
    .attr("width", 400)
    .attr("height", 400);

  svg
    .append("circle")
    .attr("cx", 200)
    .attr("cy", 200)
    .attr("r", 50)
    .style("fill", "steelblue")
    .transition()
    .duration(1000)
    .attr("r", 80)
    .style("fill", "orange");
});
