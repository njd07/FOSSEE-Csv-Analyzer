import React from 'react';

// Scrollable data table
function EquipmentTable({ rows }) {
    if (!rows || !rows.length) return null;
    const cols = Object.keys(rows[0]);

    return (
        <div className="card">
            <h2>Equipment Data</h2>
            <div className="table-scroll">
                <table className="data-table">
                    <thead>
                        <tr>{cols.map(c => <th key={c}>{c}</th>)}</tr>
                    </thead>
                    <tbody>
                        {rows.map((row, i) => (
                            <tr key={i}>{cols.map(c => <td key={c}>{row[c]}</td>)}</tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default EquipmentTable;
