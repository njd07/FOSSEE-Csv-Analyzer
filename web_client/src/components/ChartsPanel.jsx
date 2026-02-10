import React from 'react';
import { Bar, Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS, CategoryScale, LinearScale, BarElement,
    RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend
} from 'chart.js';

// Register chart components
ChartJS.register(CategoryScale, LinearScale, BarElement, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

// Bar + Radar charts
function ChartsPanel({ chartData }) {
    if (!chartData) return null;
    const { labels, counts, averages } = chartData;

    const barData = {
        labels,
        datasets: [{ label: 'Count', data: counts, backgroundColor: '#3b6cb4', borderRadius: 3 }]
    };

    const radarData = {
        labels: Object.keys(averages),
        datasets: [{
            label: 'Averages',
            data: Object.values(averages),
            backgroundColor: 'rgba(59,108,180,0.15)',
            borderColor: '#3b6cb4',
            pointBackgroundColor: '#3b6cb4'
        }]
    };

    return (
        <div className="card">
            <h2>Charts</h2>
            <div className="chart-grid">
                <div className="chart-box">
                    <h3>Type Distribution</h3>
                    <Bar data={barData} options={{ responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }} />
                </div>
                <div className="chart-box">
                    <h3>Parameter Averages</h3>
                    <Radar data={radarData} options={{ responsive: true, scales: { r: { beginAtZero: true } } }} />
                </div>
            </div>
        </div>
    );
}

export default ChartsPanel;
