import { drivers } from "../data/sources/driversJSON.js";
import * as elements from './elements.js';

export function render(driverNumber) {
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
