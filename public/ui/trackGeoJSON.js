
export async function renderGeoJSON(locationId, container) {
    // Clear the previous SVG content
    const geojsonFile = `/f1-circuits/circuits/${locationId}.geojson`;

    container.innerHTML = '';

    const width = 400;
    const height = 400;

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);


    d3.json(geojsonFile).then(data => {
        const projection = d3.geoMercator().fitSize([width, height], data);
        const path = d3.geoPath().projection(projection);

        svg.append('path')
            .datum(data)
            .attr('d', path)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2);
    });
}