import pandas as pd

# Cesta k souboru
file_path = "LEK13_202509v01.csv"

# Načtení CSV s kódováním Windows-1250 a středníkem jako oddělovačem
df = pd.read_csv(file_path, encoding="windows-1250", sep=";")

# Smazání zadaných sloupců, pokud existují
columns_to_drop = [
    "Období",
    "Držitel registrace",
    "Země",
    "Nákupní cena bez DPH",
    "Konečná prodejní cena s DPH",
    "Způsob výdeje",
    "Hrazeno",
]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Filtrování řádků, kde Typ hlášení == 'recept'
df = df[df.iloc[:, 0].astype(str).str.lower() != "žádanka"]

# Nahrazení desetinných čárek tečkami a převod na čísla
if "Počet balení" in df.columns:
    df["Počet balení"] = (
        df["Počet balení"].astype(str).str.replace(",", ".").astype(float)
    )

# Sumarizace podle ATC7
if "ATC7" in df.columns:
    summary = df.groupby("ATC7", as_index=False)["Počet balení"].sum()
    summary = summary.sort_values(by="Počet balení", ascending=False)

# Výběr prvních 10 řádků
top10 = summary.head(10)

print(top10)
