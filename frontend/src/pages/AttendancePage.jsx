import React, { useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";
import "../styles.css";

export default function AttendancePage() {
  const [empId, setEmpId] = useState("");
  const [date, setDate] = useState("");
  const [status, setStatus] = useState("present");
  const [records, setRecords] = useState([]);
  const [message, setMessage] = useState("");

  // Load attendance history for a given employee
  const load = async (id) => {
    try {
      const res = await axios.get(`http://localhost:5000/attendance/${id}`);
      setRecords(res.data || []);
      setMessage(`Loaded ${res.data.length} record(s)`);
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Failed to load attendance records");
    }
  };

  // Mark new attendance
  const mark = async () => {
    if (!empId || !date) {
      setMessage("⚠️ Please enter both Employee ID and Date");
      return;
    }
    try {
      const res = await axios.post("http://localhost:5000/attendance", {
        emp_id: parseInt(empId),
        date,
        status,
      });

      if (res.data.error) {
        setMessage(`❌ ${res.data.error}`);
      } else {
        setMessage(`✅ Marked ${status} for employee ${empId} on ${date}`);
        load(empId); // reload table
      }
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Network or server error while marking attendance");
    }
  };

  return (
    <div className="page">
      <h2>Attendance</h2>

      {/* ===== Attendance Form ===== */}
      <div className="form">
        <input
          placeholder="Employee ID"
          value={empId}
          onChange={(e) => setEmpId(e.target.value)}
          type="number"
        />
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="present">Present</option>
          <option value="absent">Absent</option>
          <option value="late">Late</option>
        </select>
        <button onClick={mark}>Mark</button>
        <button onClick={() => load(empId)}>View Records</button>
      </div>

      {/* ===== Status Message ===== */}
      {message && (
        <div
          style={{
            backgroundColor: message.startsWith("✅")
              ? "#e6ffed"
              : message.startsWith("⚠️")
              ? "#fff7e6"
              : message.startsWith("❌")
              ? "#ffe6e6"
              : "#f5f5f5",
            borderLeft: "5px solid #0078d7",
            padding: "0.6rem 1rem",
            borderRadius: "6px",
            marginBottom: "1rem",
            color: "#333",
            fontWeight: "500",
          }}
        >
          {message}
        </div>
      )}

      {/* ===== Attendance Records Table ===== */}
      <TableView
        headers={["ID", "Emp_id", "Date", "Status"]}
        rows={records.map((r) => ({
          id: r.id,
          emp_id: r.emp_id,
          date: r.date,
          status:
            r.status === "present"
              ? "✅ Present"
              : r.status === "absent"
              ? "❌ Absent"
              : "⏰ Late",
        }))}
      />
    </div>
  );
}
