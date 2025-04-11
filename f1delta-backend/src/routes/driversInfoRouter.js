import express from "express";

const router = express.Router();

router.get("/", async (req, res) => {
  const { driver_number, session_key } = req.query;

  if (!driver_number || !session_key) {
    return res.status(400).json({ error: "Missing driver_number or session_key" });
  }

  try {
    const url = `https://api.openf1.org/v1/drivers?driver_number=${driver_number}&session_key=${session_key}`;
    const response = await fetch(url); // Native fetch in Node 18+
    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error("Error fetching driver info:", error);
    res.status(500).json({ error: "Failed to fetch driver info" });
  }
});

export default router;
