import React, { useEffect, useState } from "react";
import axios from "axios";

export default function NotificationPage() {
  const [notes, setNotes] = useState([]);

  const load = async () => {
    const res = await axios.get("http://localhost:5000/notifications");
    setNotes(res.data.reverse());
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="page">
      <h2>Recent Notifications</h2>
      <ul>
        {notes.map((n, i) => (
          <li key={i}>{n}</li>
        ))}
      </ul>
    </div>
  );
}
