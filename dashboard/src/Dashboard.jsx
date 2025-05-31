import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [countries, setCountries] = useState([]);
  const [pandemics, setPandemics] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedPandemic, setSelectedPandemic] = useState(null);
  const [statType, setStatType] = useState('daily_new_cases');
  const [stats, setStats] = useState({});
  const [startDate, setStartDate] = useState("2020-01-01");
  const [endDate, setEndDate] = useState("2025-01-01");
  const [transmissionRate, setTransmissionRate] = useState(0);
  const [mortalityRate, setMortalityRate] = useState(0);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/country').then(res => setCountries(res.data));
    axios.get('http://127.0.0.1:5000/pandemic').then(res => setPandemics(res.data));
  }, []);

  useEffect(() => {
    if (selectedCountry && selectedPandemic) {
      axios
        .get(`http://127.0.0.1:5000/pandemic_country/${selectedCountry}/${selectedPandemic}`)
        .then(res => {
          setStats(res.data);
          const { total_deaths, total_confirmed } = res.data;
          const rate = total_confirmed ? (total_deaths / total_confirmed) * 100 : 0;
          setMortalityRate(rate.toFixed(2));
        });

      axios
        .get(`http://127.0.0.1:5000/daily_pandemic_country/${selectedCountry}/${selectedPandemic}`)
        .then(res => {
          const data = res.data.filter(entry => {
            const date = new Date(entry.date);
            return date >= new Date(startDate) && date <= new Date(endDate);
          });

          const totalCases = data.reduce((sum, item) => sum + (item.daily_new_cases || 0), 0);
          const meanActive = data.reduce((sum, item) => sum + (item.active_cases || 0), 0) / (data.length || 1);

          const transmission = meanActive ? (totalCases / meanActive) * 100 : 0;
          setTransmissionRate(transmission.toFixed(2));
        });
    }
  }, [selectedCountry, selectedPandemic, startDate, endDate]);

  return (
    <div className="p-4 text-black">
      <h1 className="text-3xl font-bold mb-4 text-center">Pandemic Dashboard</h1>

      <div className="flex flex-wrap gap-4 justify-center mb-6">
        <select
          className="w-40 h-30 p-2 rounded bg-gray-800 text-white text-center appearance-none"
          onChange={e => setSelectedCountry(e.target.value)}
          defaultValue=""
        >
          <option value="" disabled>Select Country</option>
          {countries.map(([id, name]) => (
            <option key={id} value={id}>{name}</option>
          ))}
        </select>

        <select
          className=" w-40 h-30 p-2 rounded bg-gray-800 text-white text-center appearance-none"
          onChange={e => setSelectedPandemic(e.target.value)}
          defaultValue=""
        >
          <option value="" disabled>Select Pandemic</option>
          {pandemics.map(p => (
            <option key={p.id_pandemic} value={p.id_pandemic}>{p.name}</option>
          ))}
        </select>

        <select
          className="w-40 h-30 p-2 rounded bg-gray-800 text-white text-center appearance-none"
          onChange={e => setStatType(e.target.value)}
          value={statType}
        >
          <option value="daily_new_cases">Cases</option>
          <option value="daily_new_deaths">Deaths</option>
        </select>

        <input
          type="date"
          value={startDate}
          onChange={e => setStartDate(e.target.value)}
          className="w-40 h-30 p-2 rounded bg-gray-800 text-white text-center appearance-none"
        />
        <input
          type="date"
          value={endDate}
          onChange={e => setEndDate(e.target.value)}
          className="w-40 h-30 p-2 rounded bg-gray-800 text-white text-center appearance-none"
        />
      </div>

      {/* Stat Cards */}
      <div className="flex flex-wrap justify-center gap-4">
        <div className="w-40 h-28 p-4 bg-primary text-primary-foreground rounded shadow">
          <h3 className="text-lg font-semibold">Total Confirmed</h3>
          <p className="text-2xl font-bold">{stats.total_confirmed || 0}</p>
        </div>
        <div className="w-40 h-28 p-4 bg-destructive text-destructive-foreground rounded shadow">
          <h3 className="text-lg font-semibold">Total Deaths</h3>
          <p className="text-2xl font-bold">{stats.total_deaths || 0}</p>
        </div>
        <div className="w-40 h-28 p-4 bg-accent text-accent-foreground rounded shadow">
          <h3 className="text-lg font-semibold">Total Recovered</h3>
          <p className="text-2xl font-bold">{stats.total_recovered || 0}</p>
        </div>
        <div className="w-40 h-28 p-4 bg-muted text-muted-foreground rounded shadow">
          <h3 className="text-lg font-semibold">Mortality Rate</h3>
          <p className="text-2xl font-bold">{mortalityRate}%</p>
        </div>
        <div className="w-40 h-28 p-4 bg-muted text-muted-foreground rounded shadow">
          <h3 className="text-lg font-semibold">Transmission Rate</h3>
          <p className="text-2xl font-bold">{transmissionRate}%</p>
        </div>
      </div>
    </div>
  );
}
