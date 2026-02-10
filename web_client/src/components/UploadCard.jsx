import React, { useState } from 'react';
import axios from 'axios';

// File upload card
function UploadCard({ token, api, onSuccess }) {
    const [file, setFile] = useState(null);
    const [busy, setBusy] = useState(false);
    const [msg, setMsg] = useState('');

    const upload = async () => {
        if (!file) { setMsg('Select a CSV file.'); return; }
        setBusy(true); setMsg('Uploading...');
        const fd = new FormData();
        fd.append('file', file);
        try {
            const r = await axios.post(`${api}/upload/`, fd, {
                headers: { Authorization: `Token ${token}`, 'Content-Type': 'multipart/form-data' }
            });
            setMsg(`Uploaded: ${r.data.name}`);
            onSuccess(r.data);
        } catch (err) { setMsg(err.response?.data?.error || 'Upload failed.'); }
        finally { setBusy(false); }
    };

    return (
        <div className="card">
            <h2>Upload CSV</h2>
            <div className="upload-row">
                <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} />
                <button className="btn" onClick={upload} disabled={busy}>{busy ? 'Uploading...' : 'Upload'}</button>
            </div>
            {msg && <p className="status-text">{msg}</p>}
        </div>
    );
}

export default UploadCard;
