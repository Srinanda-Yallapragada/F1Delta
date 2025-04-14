import { drivers, driverIds, driversJSON } from './driversJSON.js'
import { getDriverInfo } from "./api_calls.js";
import { selectElement } from '../../ui/elements.js';

export async function loadDriverData() {
    for (const driver of driversJSON) {
        const info = await getDriverInfo(driver.number);
        const updated = { ...driver, ...info };
        // console.log(`got info for ${driver.name}`, updated);
        drivers[driver.number] = updated;
        driverIds.push(driver.number);


        const option = document.createElement("option");
        option.value = driver.number;
        option.textContent = updated.name;
        selectElement.appendChild(option);
    }

}