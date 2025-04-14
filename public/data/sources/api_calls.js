import { getIdFromLocation } from "./localJSON.js";


const OPENF1_API_URL = 'https://api.openf1.org/v1';
const JOLPI_API_URL = 'http://api.jolpi.ca/ergast/f1'


export async function getDriverInfo(driver_number, session_key = 'latest') {
    const res = await fetch(`${OPENF1_API_URL}/drivers?` + new URLSearchParams({
        driver_number: driver_number,
        session_key: session_key,
    }))
    return (await res.json())[0];
}

export async function getCompletedRaces2025() {
    const res = await fetch(`${OPENF1_API_URL}/sessions?session_name=Race&year=2025`);
    return (await res.json())
}


export const completedRaces2025 = await getCompletedRaces2025();



