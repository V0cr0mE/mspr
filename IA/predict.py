import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# --- Paramètres ---
csv_path = "C:/Users/Anes/MSPR/donnes_clean/worldometer_coronavirus_daily_data_clean.csv" 
country = "Switzerland"  

# --- Étape 1 : Charger et préparer les données ---
print(f"Chargement des données pour {country}")
data = pd.read_csv(csv_path)
data['date'] = pd.to_datetime(data['date'])

country_data = data[data['country'] == country].copy()
country_data.sort_values('date', inplace=True)
country_data.reset_index(drop=True, inplace=True)

# Créer les features glissantes (lags)
for i in range(1, 8):
    country_data[f'lag_{i}'] = country_data['daily_new_cases'].shift(i)

country_data.dropna(inplace=True)

X = country_data[[f'lag_{i}' for i in range(1, 8)]]
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

# --- Étape 4 : Prédiction sur le jour suivant ---
dernieres_valeurs = country_data['daily_new_cases'].iloc[-7:].values.reshape(1, -1)
prediction = model.predict(dernieres_valeurs)

print(f"Prédiction pour le jour suivant ({country}) : {int(prediction[0])} cas")
