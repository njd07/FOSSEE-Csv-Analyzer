import React from 'react';

function SummaryPanel({ summary }) {
    if (!summary) return null;
    const { total_count, averages, type_distribution } = summary;

    return (
        <div className="card">
            <h2>Summary</h2>
            <div className="stats">
                <div className="stat">
                    <div className="stat-val">{total_count}</div>
                    <div className="stat-label">Total Rows</div>
                </div>
                {averages && Object.entries(averages).map(([k, v]) => (
                    <div className="stat" key={k}>
                        <div className="stat-val">{v}</div>
                        <div className="stat-label">Avg {k}</div>
                    </div>
                ))}
            </div>
            {type_distribution && (
                <p className="status-text mt">
                    Types: {Object.entries(type_distribution).map(([t, c]) => `${t} (${c})`).join(', ')}
                </p>
            )}
        </div>
    );
}

export default SummaryPanel;
