import React from 'react';

// List of last 5 uploads
function HistoryPanel({ history, onSelect }) {
    if (!history || !history.length) return null;

    return (
        <div className="card">
            <h2>Upload History</h2>
            <ul className="history-list">
                {history.map(item => (
                    <li key={item.id} className="history-item">
                        <span><strong>{item.name}</strong> — {item.row_count} rows</span>
                        <div>
                            <span style={{ marginRight: 8, color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                                {new Date(item.uploaded_at).toLocaleString()}
                            </span>
                            <button className="btn btn-small" onClick={() => onSelect(item)}>View</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default HistoryPanel;
