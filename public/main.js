import './data/locations.js'
import { getDriverInfo } from './data/sources/openf1.js';
import { drivers, driverIds, driversJSON } from './data/sources/driversJSON.js';
import { generateTrackSvgHtml } from "./ui/trackSVG.js"
import { renderGeoJSON } from './ui/trackGeoJSON.js';
import { loadDriverData } from './data/sources/loadDriverData.js';
import { render } from './ui/render.js';
import * as elements from "./ui/elements.js";


async function init() {

    // This loop creates the drop down options and  populates the drivers object
    await loadDriverData();

    // Adds track cards 
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

    // On dropdown select change, this function 
    elements.selectElement.onchange = function (event) {
        render(event.target.value);
    }

    render(1); // load max verstappen (driver 1) by default
}

init();
// window.onload = init;
// window.addEventListener("load", () => console.log("bar"));
