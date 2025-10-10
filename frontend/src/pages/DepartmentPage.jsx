import React, { useEffect, useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";

export default function DepartmentPage() {
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");

  const load = async () => {
    try {
      const res = await axios.get("http://localhost:5000/departments");
      setDepartments(res.data || []);
    } catch (err) {
      console.error(err);
      alert("Failed to load departments.");
    }
  };

  const create = async () => {
    if (!name.trim()) return alert("Enter department name");
    try {
      await axios.post("http://localhost:5000/departments", {
        name,
        location: location || undefined,
      });
      setName("");
      setLocation("");
      load();
    } catch (err) {
      console.error(err);
      alert("Failed to add department.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`Delete department ${id}?`)) return;
    try {
      await axios.delete(`http://localhost:5000/department/delete/${id}`);
      load();
    } catch (err) {
      console.error(err);
      alert("Error deleting department.");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const rows = departments.map((d) => [
    d.id,
    d.name,
    (d.employees || []).length,
    <button
      key={`del-${d.id}`}
      onClick={() => handleDelete(d.id)}
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
      <h2>Departments</h2>

      <div className="form" style={{ marginBottom: 15, display: "flex", gap: 8 }}>
        <input
          placeholder="Department name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          placeholder="Location (optional)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <button onClick={create}>Add</button>
      </div>

      <TableView
        headers={["ID", "Name", "Employees", "Action"]}
        rows={rows}
      />
    </div>
  );
}
