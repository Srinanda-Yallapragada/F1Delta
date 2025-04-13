import { getDriverInfo } from './openf1_api_calls/driverInfo.js';

const driversJSON = [
  { number: 1, name: "Max Verstappen" },
  { number: 4, name: "Lando Norris" },
  { number: 10, name: "Pierre Gasly" },
  { number: 14, name: "Fernando Alonso" },
  { number: 16, name: "Charles Leclerc" },
  { number: 18, name: "Lance Stroll" },
  { number: 22, name: "Yuki Tsunoda" },
  { number: 23, name: "Alexander Albon" },
  { number: 27, name: "Nico Hülkenberg" },
  { number: 31, name: "Esteban Ocon" },
  { number: 44, name: "Lewis Hamilton" },
  { number: 55, name: "Carlos Sainz" },
  { number: 63, name: "George Russell" },
  { number: 81, name: "Oscar Piastri" },
];

const drivers = {}

const selectElement = document.getElementById("driver-selector"); //This is the drop down
const selectedDriver = document.getElementById("selected-driver"); //This is the text 
const selectedDriverImg = document.getElementById("driver-image"); //This is the image

// This loop creates the drop down options
driversJSON.forEach(driver => {
  const option = document.createElement("option");
  option.value = driver.number;
  option.textContent = driver.name;
  drivers[driver.number] = driver.name;
  selectElement.appendChild(option);
});

// On change, this function 
selectElement.onchange = async function (event) {
  const driverNumber = event.target.value;
  const driverInfo = await getDriverInfo(driverNumber);
  selectedDriver.textContent = `Selected Driver: ${driverInfo.driver_number}  ${driverInfo.full_name}`;
  selectedDriverImg.src = driverInfo.headshot_url;
}