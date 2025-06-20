import React from 'react';
import Plot from 'react-plotly.js';

export default function Histogram({ predictionData, statType }) {
    return (
        <div>
            <h2 className="text-2xl font-bold mb-2">
                Prédictions 7 jours : {statType === 'daily_new_cases' ? 'Cas quotidiens' : 'Décès quotidiens'}
            </h2>
            {predictionData.length === 0 ? (
                <p>Aucune donnée pour cet histogramme.</p>
            ) : (
                <div className="w-full h-64 md:h-80 lg:h-96">
                    <Plot
                        data={[
                            {
                                x: predictionData.map(d => d.date),
                                y: predictionData.map(d =>
                                    statType === 'daily_new_cases'
                                        ? d.predicted_cases || 0
                                        : d.predicted_deaths || 0
                                ),
                                type: 'bar',
                                marker: { color: 'tomato' }
                            }
                        ]}
                        layout={{
                            barmode: 'overlay',
                            paper_bgcolor: '#1f2937',
                            plot_bgcolor: '#1f2937',
                            font: { color: '#ffffff' },
                            xaxis: { title: 'Date', gridcolor: '#374151', color: '#ffffff' },
                            yaxis: { title: 'Nombre', gridcolor: '#374151', color: '#ffffff' },
                            margin: { l: 40, r: 20, t: 40, b: 40 }
                        }}
                        style={{ width: '100%', height: '100%' }}
                    />
                </div>
            )}
        </div>
    );
}