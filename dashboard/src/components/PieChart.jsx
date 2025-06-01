import React from 'react';
import Plot from 'react-plotly.js';

export default function PieChart({ byContinent, statType }) {
    return (
        <div>
            <h2 className="text-2xl font-bold mb-2">
                Répartition par continent ({statType === 'daily_new_cases' ? 'Cas' : 'Décès'})
            </h2>
            {byContinent.length === 0 ? (
                <p>Aucune donnée continentale.</p>
            ) : (
                <Plot
                    data={[
                        {
                            labels: byContinent.map(c => c.continent),
                            values: byContinent.map(c =>
                                statType === 'daily_new_cases' ? c.total_confirmed : c.total_deaths
                            ),
                            type: 'pie',
                            hole: 0.3,
                            textinfo: 'percent+label',
                            pull: byContinent.map(() => 0.05)
                        }
                    ]}
                    layout={{
                        paper_bgcolor: '#1f2937',
                        plot_bgcolor: '#1f2937',
                        font: { color: '#ffffff' },
                        margin: { l: 20, r: 20, t: 40, b: 20 }
                    }}
                    style={{ width: '100%', height: '400px' }}
                />
            )}
        </div>
    );
}