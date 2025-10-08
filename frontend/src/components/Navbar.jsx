import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/">Employees</Link>
      <Link to="/departments">Departments</Link>
      <Link to="/attendance">Attendance</Link>
      <Link to="/payroll">Payroll</Link>
      <Link to="/notifications">Notifications</Link>
    </nav>
  );
}
