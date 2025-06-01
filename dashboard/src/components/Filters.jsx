import React from 'react';

export default function Filters({
    countries,
    pandemics,
    selectedCountry,
    setSelectedCountry,
    selectedPandemic,
    setSelectedPandemic,
    statType,
    setStatType,
    startDate,
    setStartDate,
    endDate,
    setEndDate
}) {
    return (
        <section aria-label="Filtres" className="flex flex-wrap gap-4 justify-center mb-8">
            <div>
                <label htmlFor="country-select" className="block mb-1 font-semibold">
                    Sélection Pays
                </label>
                <select
                    id="country-select"
                    value={selectedCountry}
                    onChange={e => setSelectedCountry(e.target.value)}
                    className="p-2 rounded bg-gray-800 focus:ring-2 focus:ring-blue-500"
                >
                    <option value="" disabled>
                        -- choisir un pays --
                    </option>
                    {countries.map(c => (
                        <option key={c[0]} value={c[0]}>
                            {c[1]}
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label htmlFor="pandemic-select" className="block mb-1 font-semibold">
                    Sélection Pandémie
                </label>
                <select
                    id="pandemic-select"
                    value={selectedPandemic}
                    onChange={e => setSelectedPandemic(e.target.value)}
                    className="p-2 rounded bg-gray-800 focus:ring-2 focus:ring-blue-500"
                >
                    <option value="" disabled>
                        -- choisir une pandémie --
                    </option>
                    {pandemics.map(p => (
                        <option key={p.id_pandemic} value={p.id_pandemic}>
                            {p.name}
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label htmlFor="stat-type-select" className="block mb-1 font-semibold">
                    Type de statistique
                </label>
                <select
                    id="stat-type-select"
                    value={statType}
                    onChange={e => setStatType(e.target.value)}
                    className="p-2 rounded bg-gray-800 focus:ring-2 focus:ring-blue-500"
                >
                    <option value="daily_new_cases">Cases quotidiens</option>
                    <option value="daily_new_deaths">Décès quotidiens</option>
                </select>
            </div>

            <div>
                <label className="block mb-1 font-semibold">Période</label>
                <div className="flex gap-2">
                    <input
                        type="date"
                        value={startDate}
                        onChange={e => setStartDate(e.target.value)}
                        className="p-2 rounded bg-gray-800 focus:ring-2 focus:ring-blue-500"
                        aria-label="Date de début"
                    />
                    <input
                        type="date"
                        value={endDate}
                        onChange={e => setEndDate(e.target.value)}
                        className="p-2 rounded bg-gray-800 focus:ring-2 focus:ring-blue-500"
                        aria-label="Date de fin"
                    />
                </div>
            </div>
        </section>
    );
}