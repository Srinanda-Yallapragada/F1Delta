import express from "express";
import cors from "cors";

const app = express();
const port = "3000";

import driverInfoRouter from "./routes/driversInfoRouter.js";
import trackInfoRouter from "./routes/trackInfoRouter.js";

app.use(express.json());
app.use(cors());

app.use("/driverInfo", driverInfoRouter);
app.use("/trackInfo", trackInfoRouter);

app.listen(port, () => {
  console.log(`Listening on port http://localhost:${port}`);
});
