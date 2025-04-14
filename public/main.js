import './data/locations.js'
import { getDriverInfo } from '../data/sources/openf1.js';
import { driversJSON } from '../data/sources/driversJSON.js';
import { locationDetails2025 } from "../data/locations.js";
import { generateTrackSvgHtml } from "./ui/trackSVG.js"
import { selectTrackList, selectElement, driverNameElement, driverNumberElement, trackModal, selectedDriverImg, modalTrackImage, modalTitle, trackVisualizationContainer } from "./ui/elements.js";


function init(_) {
    generateTrackSvgHtml()

    // Add click listener to all track cards
    document.getElementsByClassName('track-card').forEach(card => {
        card.addEventListener('click', function () {
            const trackName = this.dataset.trackName;
            const trackId = this.dataset.trackId;

            modalTitle.textContent = trackName;
            renderGeoJSON(trackId, trackVisualizationContainer);
            trackModal.show();
        });
    });


    // This loop creates the drop down options
    driversJSON.forEach(driver => {
        const option = document.createElement("option");
        option.value = driver.number;
        option.textContent = driver.name;
        selectElement.appendChild(option);
    });


    async function render(driverNumber) {
        // const driverNumber = state.driverNumber;
        const driverInfo = await getDriverInfo(driverNumber);
        driverNameElement.textContent = driverInfo.full_name;
        driverNumberElement.textContent = driverInfo.driver_number;
        selectedDriverImg.src = driverInfo.headshot_url;

        document.body.style.backgroundColor = `#${driverInfo.team_colour}`;


        // from driversJSON to update the driver info with wins and other stats
        const localDriver = driversJSON.find(d => d.number == driverNumber);

        document.getElementById("wins").textContent = localDriver.wins;
        document.getElementById("poles").textContent = localDriver.poles;
        document.getElementById("podiums").textContent = localDriver.podiums;
        document.getElementById("championships").textContent = localDriver.championships;


        document.querySelectorAll('.driver-stats-24').forEach(statContainer => {
            const trackId = statContainer.dataset.trackId;
            const result = localDriver.results?.[trackId];

            statContainer.querySelector('.position').textContent = "test";
            statContainer.querySelector('.lap').textContent = "test";
            statContainer.querySelector('.points').textContent = "test";
        });

        document.querySelectorAll('.driver-stats-25').forEach(statContainer => {
            const trackId = statContainer.dataset.trackId;
            const result = localDriver.results?.[trackId];

            statContainer.querySelector('.position').textContent = "test";
            statContainer.querySelector('.lap').textContent = "test";
            statContainer.querySelector('.points').textContent = "test";
        });
    }

    // On change, this function 
    selectElement.onchange = async function (event) {
        render(event.target.value);
    }

    async function renderGeoJSON(locationId, container) {
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

    render(1);
}

init();
// window.onload = init;
// window.addEventListener("load", () => console.log("bar"));
