import express from "express";
import cors from "cors";

const app = express();
const port = "3000";

import driverInfoRouter from "./routes/driversInfoRouter.js";

app.use(express.json()); // Parse JSON bodies
app.use(cors()); // CORS for frontend requests

app.use("/driverInfo", driverInfoRouter);


app.listen(port, () => {
  console.log(`Listening on port http://localhost:${port}`);
});
