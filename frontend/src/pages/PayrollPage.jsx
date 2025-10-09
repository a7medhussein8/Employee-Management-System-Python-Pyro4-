// import React, { useState } from "react";
// import axios from "axios";
// import TableView from "../components/TableView";
// import "../styles.css";

// export default function PayrollPage() {
//   const [empId, setEmpId] = useState("");
//   const [month, setMonth] = useState("");
//   const [payroll, setPayroll] = useState(null);
//   const [history, setHistory] = useState([]);
//   const [message, setMessage] = useState("");

//   // Calculate payroll for this employee and month
//   const calc = async () => {
//     if (!empId || !month) {
//       setMessage("⚠️ Please enter Employee ID and Month");
//       return;
//     }
//     try {
//       const res = await axios.get(
//         `http://localhost:5000/payroll/${empId}/${month}`
//       );
//       if (res.data.error) {
//         setMessage(`❌ ${res.data.error}`);
//       } else {
//         setPayroll(res.data);
//         setMessage(`✅ Payroll calculated for Employee ${empId} (${month})`);
//         loadHistory(); // reload payroll history
//       }
//     } catch (err) {
//       console.error(err);
//       setMessage("⚠️ Network error while calculating payroll");
//     }
//   };

//   // Load payroll history for this employee
//   const loadHistory = async () => {
//     if (!empId) return;
//     try {
//       const res = await axios.get(
//         `http://localhost:5000/payroll/history/${empId}`
//       );
//       setHistory(res.data || []);
//     } catch (err) {
//       console.error(err);
//       setMessage("⚠️ Failed to load payroll history");
//     }
//   };

//   return (
//     <div className="page">
//       <h2>Payroll</h2>

//       {/* Form */}
//       <div className="form">
//         <input
//           placeholder="Employee ID"
//           value={empId}
//           onChange={(e) => setEmpId(e.target.value)}
//           type="number"
//         />
//         <input
//           placeholder="Month (YYYY-MM)"
//           value={month}
//           onChange={(e) => setMonth(e.target.value)}
//         />
//         <button onClick={calc}>Calculate Payroll</button>
//         <button onClick={loadHistory}>View History</button>
//       </div>

//       {/* Status message */}
//       {message && (
//         <div
//           style={{
//             backgroundColor: message.startsWith("✅")
//               ? "#e6ffed"
//               : message.startsWith("⚠️")
//               ? "#fff7e6"
//               : message.startsWith("❌")
//               ? "#ffe6e6"
//               : "#f5f5f5",
//             borderLeft: "5px solid #0078d7",
//             padding: "0.6rem 1rem",
//             borderRadius: "6px",
//             marginBottom: "1rem",
//             color: "#333",
//             fontWeight: "500",
//           }}
//         >
//           {message}
//         </div>
//       )}

//       {/* Current payroll result */}
//       {/* {payroll && (
//         <div className="card">
//           <h3>Current Payroll Result</h3>
//           <pre>{JSON.stringify(payroll, null, 2)}</pre>
//         </div>
//       )} */}

//       {/* Payroll History Table */}
//       {history.length > 0 && (
//         <div className="card">
//           <h3>Payroll History</h3>
//           <TableView
//             headers={["ID", "Emp_id", "Month", "Base", "Bonus", "Deductions", "Total"]}
//             rows={history.map((h) => ({
//               id: h.id,
//               emp_id: h.emp_id,
//               month: h.month,
//               base: `$${h.base.toFixed(2)}`,
//               bonus: `$${h.bonus.toFixed(2)}`,
//               deductions: `$${h.deductions.toFixed(2)}`,
//               total: `$${h.total.toFixed(2)}`,
//             }))}
//           />
//         </div>
//       )}
//     </div>
//   );
// }

import React, { useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";
import "../styles.css";

export default function PayrollPage() {
  const [empId, setEmpId] = useState("");
  const [month, setMonth] = useState("");
  const [salary, setSalary] = useState("");
  const [bonus, setBonus] = useState("");
  const [payroll, setPayroll] = useState(null);
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);


  // ✅ Calculate payroll via POST request
  const calcPayroll = async () => {
    if (!empId || !salary) {
      setMessage("⚠️ Please enter Employee ID and Salary!");
      return;
    }

    try {
      setLoading(true);
      const res = await axios.post("http://localhost:5000/payroll/calc", {
        emp_id: parseInt(empId),
        salary: parseFloat(salary),
        bonus: parseFloat(bonus || 0),
        month: month || "N/A",
      });

      setPayroll(res.data);
      setMessage(`✅ Payroll calculated for Employee ${empId}`);
      await loadHistory(); // reload after calc
    } catch (err) {
      console.error(err);
      setMessage("❌ Failed to calculate payroll.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Fetch payroll history
  const loadHistory = async () => {
    if (!empId) {
      setMessage(" Enter Employee ID first to view history!");
      return;
    }

    try {
      setLoading(true);
      const res = await axios.get(
        `http://localhost:5000/payroll/history/${empId}`
      );
      setHistory(res.data || []);
      if ((res.data || []).length === 0)
        setMessage(" No payroll history found for this employee.");
      else setMessage(` Loaded ${res.data.length} previous records.`);
    } catch (err) {
      console.error(err);
      setMessage(" Network error while loading history.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>Payroll Management</h2>

      {/* ─── Payroll Form ───────────────────────────── */}
      <div className="form">
        <input
          type="number"
          placeholder="Employee ID"
          value={empId}
          onChange={(e) => setEmpId(e.target.value)}
        />
        <input
          type="text"
          placeholder="Month (YYYY-MM)"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
        <input
          type="number"
          placeholder="Base Salary ($)"
          value={salary}
          onChange={(e) => setSalary(e.target.value)}
        />
        <input
          type="number"
          placeholder="Bonus ($)"
          value={bonus}
          onChange={(e) => setBonus(e.target.value)}
        />
        <div style={{ display: "flex", gap: "10px" }}>
          <button onClick={calcPayroll} disabled={loading}>
            {loading ? "Processing..." : "Calculate Payroll"}
          </button>
          <button onClick={loadHistory}>
            View History
          </button>
        </div>
      </div>

      {/* ─── Status Message ─────────────────────────── */}
      {message && (
        <div
          style={{
            marginTop: "1rem",
            backgroundColor: message.startsWith("✅")
              ? "#e6ffed"
              : message.startsWith("⚠️")
                ? "#fff7e6"
                : message.startsWith("❌")
                  ? "#ffe6e6"
                  : "#f5f5f5",
            borderLeft: "5px solid #0078d7",
            padding: "10px 15px",
            borderRadius: "8px",
            color: "#333",
          }}
        >
          {message}
        </div>
      )}

      {/* ─── Payroll Summary ─────────────────────────── */}
      {payroll && (
        <div className="card">
          <h3>Latest Payroll Summary</h3>
          <table>
            <tbody>
              <tr>
                <td><b>Employee ID:</b></td>
                <td>{payroll.emp_id}</td>
              </tr>
              <tr>
                <td><b>Salary:</b></td>
                <td>${payroll.salary}</td>
              </tr>
              <tr>
                <td><b>Bonus:</b></td>
                <td>${payroll.bonus}</td>
              </tr>
              <tr>
                <td><b>Total:</b></td>
                <td>${payroll.total}</td>
              </tr>
              <tr>
                <td><b>Date:</b></td>
                <td>{payroll.date}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* ─── Payroll History ─────────────────────────── */}
      <div className="card">
        <h3>Payroll History</h3>
        {history.length > 0 ? (
          // <TableView
          //   headers={["Date", "Month", "Base", "Bonus", "Total"]}
          //   rows={history.map((h) => ({
          //     Date: h.date || h.created_at || "-",
          //     Month: h.month || "-",
          //     Base: `$${h.base || h.salary || 0}`,
          //     Bonus: `$${h.bonus || 0}`,
          //     Total: `$${h.total || 0}`,
          //   }))}
          // />
          <TableView
            headers={["Date", "Month", "Base", "Bonus", "Total"]}
            rows={history.map((h) => ({
              Date: h.date || h.created_at || "-",
              Month: h.month || "-",
              Base: `$${h.base?.toFixed?.(2) || h.salary?.toFixed?.(2) || 0}`,
              Bonus: `$${h.bonus?.toFixed?.(2) || 0}`,
              Total: `$${h.total?.toFixed?.(2) || 0}`,
            }))}
          />
        ) : (
          <p style={{ color: "#888", marginTop: "1rem" }}>
            No previous payrolls found.
          </p>
        )}
      </div>
    </div>
  );
}
