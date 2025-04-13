import './ui/driverSelectorDropdown.js';
import './ui/trackGeoJSON.js'
import './data/locations.js'
import { getDriverInfo } from '../data/sources/openf1.js';
import { driversJSON } from '../data/sources/driversJSON.js';
import { locationDetails2025 } from "../data/locations.js";
import * as d3 from 'https://d3js.org/d3.v7.min.js'





function init(_) {

    const selectElement = document.getElementById("driver-selector"); //This is the drop down
    const driverNameElement = document.getElementById("driver-name"); //This is the text 
    const driverNumberElement = document.getElementById("driver-number"); //This is the text 
    const selectedDriverImg = document.getElementById("driver-image"); //This is the image
    const selectTrackList = document.getElementById("track-list");

    const trackModal = new bootstrap.Modal(document.getElementById('trackModal'));
    const modalTrackImage = document.getElementById('modal-track-image');
    const modalTitle = document.getElementById('trackModalLabel');


    locationDetails2025.forEach(location => {
        const geojsonFilename = `/f1-circuits/circuits/${location.id}.geojson`;
        const svgFilename = `/f1-circuits/svgs/${location.id}.svg`;

        const trackHTML = `
            <div class="row pb-3">
                <div class="card track-card" track-id="${location.id}" track-name="${location.name}">
                    <div class="card-body">
                        <div class="card-title text-center mb-3">${location.name}</div>
                        <div class="row align-items-center">
                            

                            <div class="col-md-3 text-start">
                                <h6>2024</h6>
                                <p>Position: 1st</p>
                                <p>Fastest Lap: 1:23.456</p>
                                <p>Points Gained: 25</p>
                            </div>
    
                            
                            <div class="col-md-6 text-center">
                                <img src="${svgFilename}" alt="${location.id} track" class="img-fluid track-image"/>
                            </div>
    
                            <div class="col-md-3 text-end">
                                <h6>2025</h6>
                                <p>Position: 2nd</p>
                                <p>Fastest Lap: 1:24.123</p>
                                <p>Points Gained: 18</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;

        selectTrackList.innerHTML += trackHTML;
    });

    // Add click listener to all track cards
    document.querySelectorAll('.track-card').forEach(card => {
        card.addEventListener('click', function () {
            const trackName = this.getAttribute('track-name');

            const trackImage = this.querySelector('.track-image');

            modalTitle.textContent = trackName;
            modalTrackImage.src = trackImage.src;

            trackModal.show();
        });
    });


    // This loop creates the drop down options
    driversJSON.forEach(driver => {
        const option = document.createElement("option");
        option.value = driver.number;
        option.textContent = driver.name;
        selectElement.appendChild(option);
    });


    async function render(driverNumber) {
        // const driverNumber = state.driverNumber;
        const driverInfo = await getDriverInfo(driverNumber);
        driverNameElement.textContent = driverInfo.full_name;
        driverNumberElement.textContent = driverInfo.driver_number;
        selectedDriverImg.src = driverInfo.headshot_url;

        document.body.style.backgroundColor = `#${driverInfo.team_colour}`;


        // from driversJSON to update the driver info with wins and other stats
        const localDriver = driversJSON.find(d => d.number == driverNumber);

        document.getElementById("wins").textContent = localDriver.wins;
        document.getElementById("poles").textContent = localDriver.poles;
        document.getElementById("podiums").textContent = localDriver.podiums;
        document.getElementById("championships").textContent = localDriver.championships;

    }

    // On change, this function 
    selectElement.onchange = async function (event) {
        render(event.target.value);
    }

    render(1);
}

init();
// window.onload = init;
// window.addEventListener("load", () => console.log("bar"));
