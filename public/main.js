import './data/locations.js'
import { getDriverInfo } from './data/sources/openf1.js';
import { drivers, driverIds, driversJSON } from './data/sources/driversJSON.js';
import { generateTrackSvgHtml } from "./ui/trackSVG.js"
import { renderGeoJSON } from './ui/trackGeoJSON.js';
import { loadDriverData } from './data/sources/loadDataInInit.js';
import * as elements from "./ui/elements.js";


async function init(_) {
    // This loop creates the drop down options
    // This populates the drivers object

    await loadDriverData();
    generateTrackSvgHtml();

    // Add click listener to all track cards
    const modal = bootstrap.Modal.getOrCreateInstance('#trackModal');
    document.querySelectorAll('.track-card').forEach(card => {
        card.addEventListener('click', function () {
            const trackName = this.dataset.trackName;
            const trackId = this.dataset.trackId;

            elements.modalTitle.textContent = trackName;
            renderGeoJSON(trackId, elements.trackVisualizationContainer);
            modal.show();
        });
    });

    async function render(driverNumber) {
        const driverStatsElements24 = document.querySelectorAll('.driver-stats-24');
        const driverStatsElements25 = document.querySelectorAll('.driver-stats-25');

        // const driverNumber = state.driverNumber;
        const driverInfo = drivers[driverNumber];

        elements.driverNameElement.textContent = driverInfo.full_name;
        elements.driverNumberElement.textContent = `Driver No. ${driverInfo.driver_number}`;
        elements.selectedDriverImg.src = driverInfo.headshot_url;

        document.body.style.backgroundColor = `#${driverInfo.team_colour}`;


        elements.wins.textContent = driverInfo.wins;
        elements.poles.textContent = driverInfo.poles;
        elements.podiums.textContent = driverInfo.podiums;
        elements.championships.textContent = driverInfo.championships;


        driverStatsElements24.forEach(statContainer => {
            const trackId = statContainer.dataset.trackId;
            const result = driverInfo.results?.[trackId];

            statContainer.querySelector('.position').textContent = "test";
            statContainer.querySelector('.lap').textContent = "test";
            statContainer.querySelector('.points').textContent = "test";
        });

        driverStatsElements25.forEach(statContainer => {
            const trackId = statContainer.dataset.trackId;
            const result = driverInfo.results?.[trackId];

            statContainer.querySelector('.position').textContent = "test";
            statContainer.querySelector('.lap').textContent = "test";
            statContainer.querySelector('.points').textContent = "test";
        });
    }

    // On change, this function 
    elements.selectElement.onchange = async function (event) {
        render(event.target.value);
    }

    render(1);
}

init();
// window.onload = init;
// window.addEventListener("load", () => console.log("bar"));
