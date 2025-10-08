import React, { useEffect, useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";

export default function DepartmentPage() {
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState("");

  const load = async () => {
    const res = await axios.get("http://localhost:5000/departments");
    setDepartments(res.data);
  };

  const create = async () => {
    await axios.post("http://localhost:5000/departments", { name });
    setName("");
    load();
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="page">
      <h2>Departments</h2>
      <div className="form">
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Department name"
        />
        <button onClick={create}>Add</button>
      </div>

      <TableView
        headers={["ID", "Name", "Employees"]}
        rows={departments.map(d => ({
          id: d.id,
          name: d.name,
          employees: (d.employees || []).length,
        }))}
      />
    </div>
  );
}
