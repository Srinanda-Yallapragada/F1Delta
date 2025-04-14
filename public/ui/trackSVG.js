import { selectTrackList } from "./elements.js"

export function generateTrackSvgHtml() {

    locationDetails2025.forEach(location => {
        const geojsonFilename = `/f1-circuits/circuits/${location.id}.geojson`;
        const svgFilename = `/f1-circuits/svgs/${location.id}.svg`;

        const trackHTML = `
                <div class="row pb-3">
                    <div class="card track-card" data-track-id="${location.id}" data-track-name="${location.name}">
                        <div class="card-body">
                            <div class="card-title text-center mb-3">${location.name}</div>
                            <div class="row align-items-center">
                                
    
                                <div class="col-md-3 text-start driver-stats-24">
                                    <h6>2024</h6>
                                        <p class="position">Position: </p>
                                        <p class="lap">Fastest Lap: </p>
                                        <p class="points">Points Gained: </p>
                                </div>
        
                                
                                <div class="col-md-6 text-center">
                                    <img src="${svgFilename}" alt="${location.id} track" class="img-fluid track-image"/>
                                </div>
        
                                <div class="col-md-3 text-end driver-stats-25">
                                    <h6>2025</h6>
                                        <p class="position">Position: </p>
                                        <p class="lap">Fastest Lap: </p>
                                        <p class="points">Points Gained: </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;

        selectTrackList.innerHTML += trackHTML;
    });
}

