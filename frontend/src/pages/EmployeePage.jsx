import React, { useEffect, useState } from "react";
import axios from "axios";
import TableView from "../components/TableView";


export default function EmployeePage() {
    const [employees, setEmployees] = useState([]);
    const [name, setName] = useState("");

    const load = async () => {
        const res = await axios.get("http://localhost:5000/employees");
        setEmployees(res.data);
    };

    const create = async () => {
        await axios.post("http://localhost:5000/employees", { name });
        setName("");
        load();
    };

    useEffect(() => { load(); }, []);

    return (
        <div className="page">
            <h2>Employees</h2>
            <div className="form">
                <input value={name} onChange={e => setName(e.target.value)} placeholder="New employee name" />
                <button onClick={create}>Add</button>
            </div>
            <ul>
                {employees.map(e => (
                    <li key={e.id}>{e.name} (Dept {e.department_id || "None"})</li>
                ))}
            </ul>
            <TableView
                headers={["ID", "Name", "Department_id"]}
                rows={employees.map(e => ({
                    id: e.id,
                    name: e.name,
                    department_id: e.department_id || "None"
                }))}
            />
        </div>
    );
}
