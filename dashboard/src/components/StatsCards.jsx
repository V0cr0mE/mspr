import React from 'react';

export default function StatsCards({ stats, mortalityRate, transmissionRate }) {
    return (
        <section aria-label="Statistiques globales" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
            <div className="p-4 bg-gray-800 rounded shadow">
                <h2 className="text-lg font-semibold">Total Cases</h2>
                <p className="text-2xl font-bold">{stats.total_confirmed}</p>
            </div>
            <div className="p-4 bg-gray-800 rounded shadow">
                <h2 className="text-lg font-semibold">Total Deaths</h2>
                <p className="text-2xl font-bold">{stats.total_deaths}</p>
            </div>
            <div className="p-4 bg-gray-800 rounded shadow">
                <h2 className="text-lg font-semibold">Total Recovered</h2>
                <p className="text-2xl font-bold">{stats.total_recovered}</p>
            </div>
            <div className="p-4 bg-gray-800 rounded shadow">
                <h2 className="text-lg font-semibold">Mortality Rate</h2>
                <p className="text-2xl font-bold">{mortalityRate}%</p>
            </div>
            <div className="p-4 bg-gray-800 rounded shadow">
                <h2 className="text-lg font-semibold">Transmission Rate</h2>
                <p className="text-2xl font-bold">{transmissionRate}%</p>
            </div>
        </section>
    );
}