const JOLPICA_API_URL = 'https://api.jolpi.ca/ergast/f1/';


/**
 * 
 * @param {String} driver_lastname // driver_lastname needs to be lowercase lastname
 */
export async function getDriverStats(driver_lastname) {
    const rest = await fetch(`${JOLPICA_API_URL}/drivers/${driver_lastname}/career.json`)
}