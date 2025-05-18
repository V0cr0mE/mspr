import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# --- Paramètres ---
csv_path = "../donnes_clean/worldometer_coronavirus_daily_data_clean.csv"
country = "France"

# --- Étape 1 : Charger et préparer les données ---
print(f"Chargement des données pour {country}")
data = pd.read_csv(csv_path)
data['date'] = pd.to_datetime(data['date'])

country_data = data[data['country'] == country].copy()
country_data.sort_values('date', inplace=True)
country_data.reset_index(drop=True, inplace=True)

# --- Calcul du taux de transmission (formule OMS glissante) ---
country_data['incidence_7d'] = country_data['daily_new_cases'].rolling(window=7).sum()
country_data['prevalence_7d'] = country_data['active_cases'].rolling(window=7).mean()
country_data['transmission_rate'] = (country_data['incidence_7d'] / country_data['prevalence_7d']) * 100
country_data['transmission_rate'] = country_data['transmission_rate'].replace([np.inf, -np.inf], 0).fillna(0)

# --- Créer les features glissantes (lags)
for i in range(1, 8):
    country_data[f'lag_{i}'] = country_data['daily_new_cases'].shift(i)

country_data.dropna(inplace=True)

# --- Sélection des features
X = country_data[[f'lag_{i}' for i in range(1, 8)] + ['transmission_rate']]
y = country_data['daily_new_cases']

# --- Étape 2 : Entraîner le modèle ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Étape 3 : Évaluer le modèle ---
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print(f"Modèle entraîné pour {country}")
print(f"RMSE : {rmse:.2f} | MAE : {mae:.2f}")

# --- Étape 4 : Prédiction pour les 7 prochains jours ---
lags = country_data['daily_new_cases'].iloc[-7:].tolist()
transmission_rate = country_data['transmission_rate'].iloc[-1]
last_date = country_data['date'].iloc[-1]

print("\nPrédiction pour les 7 prochains jours :")
for i in range(1, 8):
    date_predite = last_date + pd.Timedelta(days=i)
    X_pred = pd.DataFrame(
        [lags + [transmission_rate]],
        columns=[f'lag_{i}' for i in range(1, 8)] + ['transmission_rate']
    )
    y_next = model.predict(X_pred)[0]
    print(f"{date_predite.date()} (Jour +{i}) : {int(y_next)} cas")
    lags = lags[1:] + [y_next] 

# --- Infos supplémentaires ---
print("\nDerniers cas journaliers observés :")
print(country_data['daily_new_cases'].tail(7).to_list())
print(f"Taux de transmission actuel : {transmission_rate:.2f}")
