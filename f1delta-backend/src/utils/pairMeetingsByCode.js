function pairMeetingsByCode(meetings2024, meetings2025) {
  const map2024 = new Map();
  const map2025 = new Map();

  const isPreseasonTest = (meeting) => {
    return meeting.meeting_name.toLowerCase().includes("pre-season");
  };

  for (const m of meetings2024) {
    if (!isPreseasonTest(m)) {
      map2024.set(m.meeting_code, m);
    }
  }

  for (const m of meetings2025) {
    if (!isPreseasonTest(m)) {
      map2025.set(m.meeting_code, m);
    }
  }

  const pairedList = [];

  for (const [code, meeting2024] of map2024.entries()) {
    const meeting2025 = map2025.get(code);

    if (meeting2025) {
      pairedList.push(meeting2024, meeting2025);
    }
  }

  return pairedList;
}

export default pairMeetingsByCode;
