import { getIdFromLocation as getLocObjFromName } from "./sources/localJSON.js";
import { completedRaces2025 } from "./sources/api_calls.js";

export const locationDetails2025 = completedRaces2025.map(race => getLocObjFromName(race.location))

