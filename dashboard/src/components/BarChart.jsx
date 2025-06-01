import React from 'react';
import Plot from 'react-plotly.js';

export default function BarChart({ byContinent, statType }) {
    return (
        <div>
            <h2 className="text-2xl font-bold mb-2">
                Total par continent ({statType === 'daily_new_cases' ? 'Cas confirmés' : 'Décès'})
            </h2>
            {byContinent.length === 0 ? (
                <p>Aucune donnée pour ce bar chart.</p>
            ) : (
                <Plot
                    data={[
                        {
                            x: byContinent.map(c => c.continent),
                            y: byContinent.map(c =>
                                statType === 'daily_new_cases' ? c.total_confirmed : c.total_deaths
                            ),
                            type: 'bar',
                            marker: { color: byContinent.map(() => 'skyblue') }
                        }
                    ]}
                    layout={{
                        paper_bgcolor: '#1f2937',
                        plot_bgcolor: '#1f2937',
                        font: { color: '#ffffff' },
                        xaxis: { title: 'Continent', gridcolor: '#374151', color: '#ffffff' },
                        yaxis: { title: 'Valeur', gridcolor: '#374151', color: '#ffffff' },
                        margin: { l: 40, r: 20, t: 40, b: 40 }
                    }}
                    style={{ width: '100%', height: '400px' }}
                />
            )}
        </div>
    );
}