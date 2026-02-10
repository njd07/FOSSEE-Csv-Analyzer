import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UploadCard from './components/UploadCard';
import SummaryPanel from './components/SummaryPanel';
import EquipmentTable from './components/EquipmentTable';
import ChartsPanel from './components/ChartsPanel';
import HistoryPanel from './components/HistoryPanel';

const API = 'http://localhost:8000/api';

function App() {
    const [token, setToken] = useState(localStorage.getItem('auth_token') || '');
    const [dark, setDark] = useState(localStorage.getItem('dark_mode') === 'true');
    const [authMode, setAuthMode] = useState('login');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [dataset, setDataset] = useState(null);
    const [chartData, setChartData] = useState(null);
    const [history, setHistory] = useState([]);

    // Toggle dark class on body
    useEffect(() => {
        document.body.classList.toggle('dark', dark);
        localStorage.setItem('dark_mode', dark);
    }, [dark]);

    // Load history when token changes
    useEffect(() => { if (token) loadHistory(); }, [token]);

    const headers = () => ({ headers: { Authorization: `Token ${token}` } });

    // Login with existing account
    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const res = await axios.post(`${API}/auth/token/`, { username, password });
            setToken(res.data.token);
            localStorage.setItem('auth_token', res.data.token);
        } catch { setError('Invalid credentials.'); }
    };

    // Register new account
    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const res = await axios.post(`${API}/auth/register/`, { username, password, email });
            setToken(res.data.token);
            localStorage.setItem('auth_token', res.data.token);
        } catch (err) { setError(err.response?.data?.error || 'Registration failed.'); }
    };

    const logout = () => {
        setToken('');
        localStorage.removeItem('auth_token');
        setDataset(null);
        setChartData(null);
        setHistory([]);
    };

    const loadHistory = async () => {
        try { const r = await axios.get(`${API}/history/`, headers()); setHistory(r.data); }
        catch { /* ignore */ }
    };

    // Load chart data for a dataset
    const loadCharts = async (id) => {
        try { const r = await axios.get(`${API}/chart-data/?id=${id}`, headers()); setChartData(r.data); }
        catch { /* ignore */ }
    };

    // After upload succeeds
    const onUpload = async (ds) => { setDataset(ds); await loadCharts(ds.id); await loadHistory(); };

    // Select from history
    const onSelect = async (ds) => { setDataset(ds); await loadCharts(ds.id); };

    // Download PDF
    const downloadPdf = async () => {
        if (!dataset) return;
        try {
            const r = await axios.get(`${API}/report/?id=${dataset.id}`, { ...headers(), responseType: 'blob' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(new Blob([r.data]));
            a.download = `report_${dataset.id}.pdf`;
            a.click();
        } catch { /* ignore */ }
    };

    // Auth screen
    if (!token) {
        return (
            <div>
                <header className="header">
                    <h1>CSV Visualizer</h1>
                    <button className="btn btn-small btn-outline" onClick={() => setDark(!dark)}>
                        {dark ? 'Light Mode' : 'Dark Mode'}
                    </button>
                </header>
                <div className="container">
                    <div className="form-box card">
                        <h2>{authMode === 'login' ? 'Login' : 'Register'}</h2>
                        <form onSubmit={authMode === 'login' ? handleLogin : handleRegister}>
                            <div className="field">
                                <label>Username</label>
                                <input value={username} onChange={e => setUsername(e.target.value)} required />
                            </div>
                            {authMode === 'register' && (
                                <div className="field">
                                    <label>Email (optional)</label>
                                    <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
                                </div>
                            )}
                            <div className="field">
                                <label>Password</label>
                                <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                            </div>
                            {error && <p className="error-text">{error}</p>}
                            <button className="btn" type="submit">{authMode === 'login' ? 'Login' : 'Register'}</button>
                        </form>
                        <p className="status-text mt">
                            {authMode === 'login'
                                ? <>No account? <button className="link-btn" onClick={() => { setAuthMode('register'); setError(''); }}>Register</button></>
                                : <>Have an account? <button className="link-btn" onClick={() => { setAuthMode('login'); setError(''); }}>Login</button></>
                            }
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    // Dashboard
    return (
        <div>
            <header className="header">
                <h1>CSV Visualizer</h1>
                <div className="header-right">
                    <button className="btn btn-small btn-outline" onClick={() => setDark(!dark)}>
                        {dark ? 'Light Mode' : 'Dark Mode'}
                    </button>
                    <button className="btn btn-small" onClick={logout}>Logout</button>
                </div>
            </header>
            <div className="container">
                <UploadCard token={token} api={API} onSuccess={onUpload} />

                {dataset && (
                    <>
                        <div className="grid-2">
                            <SummaryPanel summary={dataset.summary} />
                            <div className="card">
                                <h2>Actions</h2>
                                <button className="btn" onClick={downloadPdf}>Download PDF Report</button>
                            </div>
                        </div>
                        {chartData && (
                            <>
                                <EquipmentTable rows={chartData.rows} />
                                <ChartsPanel chartData={chartData} />
                            </>
                        )}
                    </>
                )}

                <HistoryPanel history={history} onSelect={onSelect} />
            </div>
        </div>
    );
}

export default App;
