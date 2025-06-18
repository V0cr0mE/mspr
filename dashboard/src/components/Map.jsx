import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import centroids from '../assets/country_centroids.json';

export default function Map({ pandemicId, statType }) {
    const [data, setData] = useState([]);

    useEffect(() => {
        if (!pandemicId) return;
        fetch(`http://127.0.0.1:5000/daily_pandemic_country/latest/${pandemicId}`)
            .then(res => res.json())
            .then(setData)
            .catch(err => console.error('Erreur latest data:', err));
    }, [pandemicId]);

    const lons = [];
    const lats = [];
    const sizes = [];
    const texts = [];

    data.forEach(d => {
        const coords = centroids[d.country];
        if (coords) {
            lons.push(coords[0]);
            lats.push(coords[1]);
            const value = d[statType] || 0;
            // reduce scaling factor so markers don't obscure the map
            const size = Math.sqrt(value) * 0.5;
            sizes.push(size);
            texts.push(`${d.country}<br>Cas: ${d.daily_new_cases || 0}<br>Décès: ${d.daily_new_deaths || 0}`);
        }
    });

    return (
        <div className="w-full h-64 md:h-80 lg:h-96">
            <h2 className="text-2xl font-bold mb-2">Carte des {statType === 'daily_new_cases' ? 'cas quotidiens' : 'décès quotidiens'}</h2>
            {lons.length === 0 ? (
                <p>Aucune donnée pour cette carte.</p>
            ) : (
                <Plot
                    data={[{
                        type: 'scattergeo',
                        lon: lons,
                        lat: lats,
                        text: texts,
                        marker: {
                            size: sizes,
                            color: 'red',
                            opacity: 0.6,
                        }
                    }]}
                    layout={{
                        geo: {
                            projection: { type: 'natural earth' },
                            bgcolor: '#1f2937',
                            showland: true,
                            showocean: true,
                            landcolor: '#2d3748',
                            oceancolor: '#1e293b'
                        },
                        paper_bgcolor: '#1f2937',
                        plot_bgcolor: '#1f2937',
                        font: { color: '#ffffff' },
                        margin: { l: 0, r: 0, t: 0, b: 0 }
                    }}
                    style={{ width: '100%', height: '100%' }}
                />
            )}
        </div>
    );
}
