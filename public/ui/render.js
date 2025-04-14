import { drivers } from "../data/sources/driversJSON.js";
import * as elements from './elements.js';

import { MelbourneResults25 } from '../data/sources/localJSON.js'


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

        const result = MelbourneResults25.Results.find(driver => driver.number == driverNumber)// load data for each track
        console.log(result)
        statContainer.querySelector('.position').textContent = `Position finished ${result.position}`;
        statContainer.querySelector('.lap').textContent = `Fastest Lap ${result.FastestLap.Time.time}`;
        statContainer.querySelector('.points').textContent = ` Points earned ${result.points}`;
    });

    driverStatsElements25.forEach(statContainer => {
        const trackId = statContainer.dataset.trackId;
        const result = driverInfo.results?.[trackId];

        statContainer.querySelector('.position').textContent = "test";
        statContainer.querySelector('.lap').textContent = "test";
        statContainer.querySelector('.points').textContent = "test";
    });
}
