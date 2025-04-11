import express from "express";

const router = express.Router();

import pairMeetingsByCode from "../utils/pairMeetingsByCode.js";

router.get("/", async (req, res) => {
  const apiBase = "https://api.openf1.org/v1/meetings";

  try {
    const [res2024, res2025] = await Promise.all([
      fetch(`${apiBase}?year=2024`),
      fetch(`${apiBase}?year=2025`),
    ]);

    const [data2024, data2025] = await Promise.all([
      res2024.json(),
      res2025.json(),
    ]);

    const codes2024 = new Set(data2024.map((meeting) => meeting.meeting_code));
    const codes2025 = new Set(data2025.map((meeting) => meeting.meeting_code));

    const common2025Meetings = data2025.filter((meeting) =>
      codes2024.has(meeting.meeting_code)
    );

    const common2024Meetings = data2024.filter((meeting) =>
      codes2025.has(meeting.meeting_code)
    );

    const interleaved = pairMeetingsByCode(
      common2024Meetings,
      common2025Meetings
    );
    console.log(interleaved);
    res.json(interleaved);
  } catch (error) {
    console.error("Error fetching meetings:", error);
    res.status(500).json({ error: "Failed to fetch meeting info" });
  }
});

export default router;
