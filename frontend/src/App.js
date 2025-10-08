import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Navbar from "./components/Navbar";
import EmployeePage from "./pages/EmployeePage";
import DepartmentPage from "./pages/DepartmentPage";
import AttendancePage from "./pages/AttendancePage";
import PayrollPage from "./pages/PayrollPage";
import NotificationPage from "./pages/NotificationPage";
import "./styles.css";

export default function App() {
  return (
    <BrowserRouter>
      {/* <nav className="navbar">
        <Link to="/">Employees</Link>
        <Link to="/departments">Departments</Link>
        <Link to="/attendance">Attendance</Link>
        <Link to="/payroll">Payroll</Link>
        <Link to="/notifications">Notifications</Link>
      </nav> */}
      <Navbar/>
      <Routes>
        <Route path="/" element={<EmployeePage />} />
        <Route path="/departments" element={<DepartmentPage />} />
        <Route path="/attendance" element={<AttendancePage />} />
        <Route path="/payroll" element={<PayrollPage />} />
        <Route path="/notifications" element={<NotificationPage />} />
      </Routes>
    </BrowserRouter>
  );
}

