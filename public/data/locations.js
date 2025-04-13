import { getIdFromLocation } from "./sources/localJSON.js";
import { completedRaces2025 } from "./sources/openf1.js";

export const locationIds = completedRaces2025.map(race => getIdFromLocation(race.location))

