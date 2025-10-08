import React, { useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";
import "../styles.css";

export default function PayrollPage() {
  const [empId, setEmpId] = useState("");
  const [month, setMonth] = useState("");
  const [payroll, setPayroll] = useState(null);
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState("");

  // Calculate payroll for this employee and month
  const calc = async () => {
    if (!empId || !month) {
      setMessage("⚠️ Please enter Employee ID and Month");
      return;
    }
    try {
      const res = await axios.get(
        `http://localhost:5000/payroll/${empId}/${month}`
      );
      if (res.data.error) {
        setMessage(`❌ ${res.data.error}`);
      } else {
        setPayroll(res.data);
        setMessage(`✅ Payroll calculated for Employee ${empId} (${month})`);
        loadHistory(); // reload payroll history
      }
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Network error while calculating payroll");
    }
  };

  // Load payroll history for this employee
  const loadHistory = async () => {
    if (!empId) return;
    try {
      const res = await axios.get(
        `http://localhost:5000/payroll/history/${empId}`
      );
      setHistory(res.data || []);
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Failed to load payroll history");
    }
  };

  return (
    <div className="page">
      <h2>Payroll</h2>

      {/* Form */}
      <div className="form">
        <input
          placeholder="Employee ID"
          value={empId}
          onChange={(e) => setEmpId(e.target.value)}
          type="number"
        />
        <input
          placeholder="Month (YYYY-MM)"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
        <button onClick={calc}>Calculate Payroll</button>
        <button onClick={loadHistory}>View History</button>
      </div>

      {/* Status message */}
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

      {/* Current payroll result */}
      {/* {payroll && (
        <div className="card">
          <h3>Current Payroll Result</h3>
          <pre>{JSON.stringify(payroll, null, 2)}</pre>
        </div>
      )} */}

      {/* Payroll History Table */}
      {history.length > 0 && (
        <div className="card">
          <h3>Payroll History</h3>
          <TableView
            headers={["ID", "Emp_id", "Month", "Base", "Bonus", "Deductions", "Total"]}
            rows={history.map((h) => ({
              id: h.id,
              emp_id: h.emp_id,
              month: h.month,
              base: `$${h.base.toFixed(2)}`,
              bonus: `$${h.bonus.toFixed(2)}`,
              deductions: `$${h.deductions.toFixed(2)}`,
              total: `$${h.total.toFixed(2)}`,
            }))}
          />
        </div>
      )}
    </div>
  );
}

