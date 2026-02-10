import React from 'react';

function HistoryPanel({ history, onSelect, onDelete, selectedId }) {
    return (
        <div className="history-panel">
            <div className="history-header">
                <h2>📁 Upload History</h2>
                <span className="history-subtitle">Last 5 uploads</span>
            </div>
            {!history || !history.length ? (
                <div className="empty-state">
                    <div className="empty-icon">📂</div>
                    <p>No uploads yet</p>
                </div>
            ) : (
                <ul className="history-list">
                    {history.map(item => (
                        <li
                            key={item.id}
                            className={`history-item ${selectedId === item.id ? 'selected' : ''}`}
                        >
                            <div className="history-content" onClick={() => onSelect(item)}>
                                <div className="history-name">{item.name}</div>
                                <div className="history-meta">
                                    <span className="row-count">📊 {item.row_count} rows</span>
                                    <span className="upload-time">
                                        {new Date(item.uploaded_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                            <button
                                className="delete-btn"
                                onClick={(e) => { e.stopPropagation(); onDelete(item.id); }}
                                title="Delete dataset"
                                aria-label="Delete"
                            >
                                🗑️
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default HistoryPanel;
