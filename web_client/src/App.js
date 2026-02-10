import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UploadCard from './components/UploadCard';
import SummaryPanel from './components/SummaryPanel';
import EquipmentTable from './components/EquipmentTable';
import ChartsPanel from './components/ChartsPanel';
import HistoryPanel from './components/HistoryPanel';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';


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
    const [showPassword, setShowPassword] = useState(false);

    useEffect(() => {
        document.body.classList.toggle('dark', dark);
        localStorage.setItem('dark_mode', dark);
    }, [dark]);

    useEffect(() => { if (token) loadHistory(); }, [token]);

    const headers = () => ({ headers: { Authorization: `Token ${token}` } });

    // Authenticates user and gets token
    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const res = await axios.post(`${API}/auth/token/`, { username, password });
            setToken(res.data.token);
            localStorage.setItem('auth_token', res.data.token);
        } catch { setError('Invalid credentials.'); }
    };

    // Creates new user account
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

    // Fetches list of past uploads
    const loadHistory = async () => {
        try { const r = await axios.get(`${API}/history/`, headers()); setHistory(r.data); }
        catch { }
    };

    // Loads chart data for selected dataset
    const loadCharts = async (id) => {
        try { const r = await axios.get(`${API}/chart-data/?id=${id}`, headers()); setChartData(r.data); }
        catch { }
    };

    const onUpload = async (ds) => { setDataset(ds); await loadCharts(ds.id); await loadHistory(); };
    const onSelect = async (ds) => { setDataset(ds); await loadCharts(ds.id); };

    // Removes dataset permanently
    const deleteDataset = async (id) => {
        if (!window.confirm('Are you sure you want to delete this dataset?')) return;
        try {
            await axios.delete(`${API}/delete/${id}/`, headers());
            if (dataset && dataset.id === id) {
                setDataset(null);
                setChartData(null);
            }
            await loadHistory();
        } catch (err) {
            alert('Failed to delete dataset');
        }
    };

    // Generates and downloads PDF report
    const downloadPdf = async () => {
        if (!dataset) return;
        try {
            const r = await axios.get(`${API}/report/?id=${dataset.id}`, { ...headers(), responseType: 'blob' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(new Blob([r.data]));
            a.download = `report_${dataset.id}.pdf`;
            a.click();
        } catch { }
    };

    if (!token) {
        return (
            <div>
                <header className="header">
                    <h1>CSV Visualizer</h1>
                    <button className="btn btn-small btn-outline" onClick={() => setDark(!dark)}>
                        {dark ? 'Light' : 'Dark'}
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
                                <div style={{ position: 'relative' }}>
                                    <input
                                        type={showPassword ? "text" : "password"}
                                        value={password}
                                        onChange={e => setPassword(e.target.value)}
                                        required
                                        style={{ paddingRight: '2.5rem' }}
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        style={{
                                            position: 'absolute',
                                            right: '0.5rem',
                                            top: '50%',
                                            transform: 'translateY(-50%)',
                                            background: 'none',
                                            border: 'none',
                                            color: 'var(--muted)',
                                            cursor: 'pointer',
                                            padding: '0.25rem',
                                            fontSize: '0.875rem'
                                        }}
                                    >
                                        {showPassword ? '👁️' : '👁️‍🗨️'}
                                    </button>
                                </div>
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

    return (
        <div>
            <header className="header">
                <h1>CSV Visualizer</h1>
                <div className="header-right">
                    <button className="btn btn-small btn-outline" onClick={() => setDark(!dark)}>
                        {dark ? 'Light' : 'Dark'}
                    </button>
                    <button className="btn btn-small" onClick={logout}>Logout</button>
                </div>
            </header>
            <div className="dashboard">
                <aside className="sidebar">
                    <HistoryPanel history={history} onSelect={onSelect} onDelete={deleteDataset} selectedId={dataset?.id} />
                </aside>
                <main className="main-content">
                    <div className="actions-bar">
                        <UploadCard token={token} api={API} onSuccess={onUpload} />
                        {dataset && (
                            <div className="action-buttons">
                                <button className="btn" onClick={downloadPdf}>📄 Download PDF</button>
                            </div>
                        )}
                    </div>

                    {dataset && (
                        <>
                            <SummaryPanel summary={dataset.summary} />
                            {chartData && (
                                <>
                                    <ChartsPanel chartData={chartData} />
                                    <EquipmentTable rows={chartData.rows} />
                                </>
                            )}
                        </>
                    )}
                </main>
            </div>
            <footer style={{ textAlign: 'center', padding: '2rem', color: 'var(--muted)', fontSize: '0.875rem' }}>
                © {new Date().getFullYear()} FOSSEE CSV Analyzer
            </footer>
        </div>
    );
}

export default App;
