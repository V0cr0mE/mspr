import pandas as pd

# Charger les données (remplace 'data.csv' par ton fichier)
df = pd.read_csv("C:/Users/Anes/MSPR/donnes/worldometer_coronavirus_summary_data.csv")

### 1️⃣ Analyse des valeurs manquantes ###
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_data = pd.DataFrame({'Valeurs manquantes': missing_values, 'Pourcentage': missing_percentage})
print("🔍 Analyse des valeurs manquantes :")
print(missing_data[missing_data["Valeurs manquantes"] > 0].sort_values(by="Pourcentage", ascending=False))

### 2️⃣ Détection des colonnes inutiles ###
# Détecter les colonnes avec trop de valeurs manquantes (>40%)
cols_high_missing = missing_data[missing_data["Pourcentage"] > 40].index
print("\n🚨 Colonnes avec plus de 40% de valeurs manquantes :")
print(list(cols_high_missing))

# Détecter les colonnes avec une seule valeur unique
unique_values = df.nunique()
constant_columns = unique_values[unique_values == 1].index
print("\n🛑 Colonnes constantes (une seule valeur unique) :")
print(list(constant_columns))

### 3️⃣ Détection des valeurs illogiques ###
print("\n⚠️ Détection des incohérences logiques :")

# Vérifier si total_confirmed < total_recovered + total_deaths
if 'total_confirmed' in df.columns and 'total_recovered' in df.columns and 'total_deaths' in df.columns:
    incoherent_cases = df[df['total_confirmed'] < (df['total_recovered'] + df['total_deaths'])]
    print(f"Nombre de lignes incohérentes (total_confirmed < total_recovered + total_deaths) : {len(incoherent_cases)}")

# Vérifier si active_cases est bien calculé
if 'active_cases' in df.columns and 'total_confirmed' in df.columns and 'total_recovered' in df.columns and 'total_deaths' in df.columns:
    incorrect_active_cases = df[df['active_cases'] != (df['total_confirmed'] - (df['total_recovered'] + df['total_deaths']))]
    print(f"Nombre de lignes incohérentes (active_cases mal calculé) : {len(incorrect_active_cases)}")

# Vérifier si serious_or_critical > active_cases (ce qui est impossible)
if 'serious_or_critical' in df.columns and 'active_cases' in df.columns:
    serious_issue = df[df['serious_or_critical'] > df['active_cases']]
    print(f"Nombre de lignes incohérentes (serious_or_critical > active_cases) : {len(serious_issue)}")

# Vérifier si total_tests < total_confirmed (ce qui est illogique)
if 'total_tests' in df.columns and 'total_confirmed' in df.columns:
    test_issue = df[df['total_tests'] < df['total_confirmed']]
    print(f"Nombre de lignes incohérentes (total_tests < total_confirmed) : {len(test_issue)}")

print("\n✅ Analyse terminée.")
