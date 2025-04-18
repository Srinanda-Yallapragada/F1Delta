export const track_locations_2025 = await fetch('/f1-circuits/championships/f1-locations-2025.json').then(res => res.json())
export const locations = await fetch('/f1-circuits/f1-locations.json').then(res => res.json())

export const MelbourneResults25 = await fetch('/f1-circuits/race-results-25/Melbourne.json').then(res => res.json())

/**
 * @param {Array} location
 */
export function getIdFromLocation(location) {
    // return locations.find(e => e.location == location).id;
    return locations.find(e => e.location == location);

}
