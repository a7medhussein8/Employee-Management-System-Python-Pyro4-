import React, { useEffect, useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";

export default function EmployeePage() {
  const [employees, setEmployees] = useState([]);
  const [name, setName] = useState("");
  const [departmentId, setDepartmentId] = useState("");

  const load = async () => {
    try {
      const res = await axios.get("http://localhost:5000/employees");
      setEmployees(res.data || []);
    } catch (err) {
      console.error(err);
      alert("Failed to load employees.");
    }
  };

  const create = async () => {
    if (!name.trim()) return alert("Enter employee name");
    try {
      await axios.post("http://localhost:5000/employees", {
        name,
        department_id: departmentId ? parseInt(departmentId) : null,
      });
      setName("");
      setDepartmentId("");
      load();
    } catch (err) {
      console.error(err);
      alert("Failed to add employee.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`Delete employee ${id}?`)) return;
    try {
      await axios.delete(`http://localhost:5000/employee/delete/${id}`);
      load();
    } catch (err) {
      console.error(err);
      alert("Error deleting employee.");
    }
  };

  useEffect(() => {
    load();
  }, []);

  // Table rows as arrays (safer with a minimal TableView)
  const rows = employees.map((e) => [
    e.id,
    e.name,
    e.department_id ?? "None",
    <button
      key={`del-${e.id}`}
      onClick={() => handleDelete(e.id)}
      style={{
        backgroundColor: "#e53935",
        color: "white",
        border: "none",
        padding: "5px 10px",
        borderRadius: "4px",
        cursor: "pointer",
      }}
    >
      Delete
    </button>,
  ]);

  return (
    <div className="page" style={{ padding: 20 }}>
      <h2>Employees</h2>

      <div className="form" style={{ marginBottom: 15, display: "flex", gap: 8 }}>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          placeholder="Department ID (optional)"
          value={departmentId}
          onChange={(e) => setDepartmentId(e.target.value)}
        />
        <button onClick={create}>Add</button>
      </div>

      <TableView
        headers={["ID", "Name", "Department ID", "Action"]}
        rows={rows}
      />
    </div>
  );
}
