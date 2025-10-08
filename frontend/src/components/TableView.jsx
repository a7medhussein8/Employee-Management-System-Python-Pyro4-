import React from "react";
import "../styles.css";

export default function TableView({ headers, rows }) {
  return (
    <table className="data-table">
      <thead>
        <tr>
          {headers.map((h, idx) => (
            <th key={idx}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.length > 0 ? (
          rows.map((row, idx) => (
            <tr key={idx}>
              {headers.map((h, i) => (
                <td key={i}>{row[h.toLowerCase()] || "-"}</td>
              ))}
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan={headers.length} style={{ textAlign: "center" }}>
              No data
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
}
