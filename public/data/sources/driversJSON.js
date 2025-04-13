export const driversJSON = [
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

export const drivers = {}

// This populates the drivers object
driversJSON.forEach(driver => {
  drivers[driver.number] = driver.name;
});

