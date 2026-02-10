import React from 'react';
import { Doughnut, Line } from 'react-chartjs-2';
import {
    Chart as ChartJS, ArcElement, CategoryScale, LinearScale,
    PointElement, LineElement, Filler, Tooltip, Legend
} from 'chart.js';

ChartJS.register(ArcElement, CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

function ChartsPanel({ chartData }) {
    if (!chartData) return null;
    const { labels, counts, averages } = chartData;

    const doughnutData = {
        labels,
        datasets: [{
            label: 'Count',
            data: counts,
            backgroundColor: [
                'rgba(59, 130, 246, 0.8)',
                'rgba(139, 92, 246, 0.8)',
                'rgba(236, 72, 153, 0.8)',
                'rgba(251, 146, 60, 0.8)',
                'rgba(34, 197, 94, 0.8)',
            ],
            borderColor: [
                '#3b82f6',
                '#8b5cf6',
                '#ec4899',
                '#fb923c',
                '#22c55e',
            ],
            borderWidth: 3,
            hoverOffset: 10,
        }]
    };

    const lineData = {
        labels: Object.keys(averages),
        datasets: [{
            label: 'Averages',
            data: Object.values(averages),
            fill: true,
            backgroundColor: 'rgba(139, 92, 246, 0.1)',
            borderColor: '#8b5cf6',
            borderWidth: 3,
            pointBackgroundColor: '#8b5cf6',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            tension: 0.4,
        }]
    };

    const doughnutOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 15,
                    font: { size: 12, weight: '500' },
                    usePointStyle: true,
                    pointStyle: 'circle',
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                padding: 12,
                cornerRadius: 8,
                titleFont: { size: 14, weight: 'bold' },
                bodyFont: { size: 13 }
            }
        },
        cutout: '65%',
    };

    const lineOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.9)',
                padding: 12,
                cornerRadius: 8,
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(128, 128, 128, 0.1)',
                    drawBorder: false
                },
                ticks: {
                    font: { size: 11 },
                    color: '#888'
                }
            },
            x: {
                grid: { display: false },
                ticks: {
                    font: { size: 11 },
                    color: '#888'
                }
            }
        }
    };

    return (
        <div className="card">
            <h2>📊 Data Visualization</h2>
            <div className="chart-grid">
                <div className="chart-box">
                    <h3>Equipment Distribution</h3>
                    <Doughnut data={doughnutData} options={doughnutOptions} />
                </div>
                <div className="chart-box">
                    <h3>Parameter Trends</h3>
                    <Line data={lineData} options={lineOptions} />
                </div>
            </div>
        </div>
    );
}

export default ChartsPanel;
