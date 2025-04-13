import express from 'express';
import cors from 'cors';

import {router as helloRouter} from './routes/helloRouter';


const app = express();
const PORT = process.env.PORT || 3000;

// static files
app.use(express.static('public'));

// middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// routes
app.use("/hello", helloRouter);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});