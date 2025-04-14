import { getRaceResults } from "./openf1.js";
import { completedRaces2025 } from "./openf1.js";

export async function loadTrackResults(){
    console.log("hello")
    const raceResults = getRaceResults(completedRaces2025);
}