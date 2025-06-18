import React from 'react';
import Plot from 'react-plotly.js';

export default function LineChart({ dailyData, statType }) {
    return (
        <div>
            <h2 className="text-2xl font-bold mb-2">
                Évolution : {statType === 'daily_new_cases' ? 'Cas quotidiens' : 'Décès quotidiens'}
            </h2>
            {dailyData.length === 0 ? (
                <p>Aucune donnée pour cette sélection.</p>
            ) : (
                <div className="w-full h-64 md:h-80 lg:h-96">
                    <Plot
                        data={[
                            {
                                x: dailyData.map(d => d.date),
                                y: dailyData.map(d => d[statType] || 0),
                                mode: 'lines+markers',
                                line: { color: 'cyan', width: 2 },
                                marker: { color: 'orange', size: 6 }
                            }
                        ]}
                        layout={{
                            paper_bgcolor: '#1f2937',
                            plot_bgcolor: '#1f2937',
                            font: { color: '#ffffff' },
                            xaxis: { title: 'Date', gridcolor: '#374151', color: '#ffffff' },
                            yaxis: {
                                title: statType === 'daily_new_cases' ? 'Nombre de cas' : 'Nombre de décès',
                                gridcolor: '#374151',
                                color: '#ffffff'
                            },
                            margin: { l: 40, r: 20, t: 40, b: 40 }
                        }}
                        style={{ width: '100%', height: '100%' }}
                    />
                </div>
            )}
        </div>
    );
}