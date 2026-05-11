# ---------------------------------------------------------
# steuer_config.py
# Zentrale Steuer-Konfiguration für Haushalts-Kompass
# ---------------------------------------------------------

# Aktuelle Steuersätze (können jederzeit geändert werden)
STEUERSAETZE = {
    "19": 0.19,
    "7": 0.07,
    "0": 0.00
}

# Automatische Steuer-Vorschläge pro Kategorie
# (K3 = automatisch + überschreibbar)
KATEGORIE_STEUER = {
    # 19% Standardsteuersatz
    "Haushalt": "19",
    "Elektronik": "19",
    "Dienstleistungen": "19",
    "Haushaltswaren": "19",
    "Handwerker": "19",
    "Auto": "19",
    "Garten": "19",

    # 7% ermäßigter Satz
    "Lebensmittel": "7",
    "Bücher": "7",
    "Zeitschriften": "7",

    # 0% steuerfrei
    "Miete": "0",
    "Versicherung": "0",
    "Gebühren": "0",
    "Bank": "0",
    "Spenden": "0",
    "Gesundheit": "0"
}

# ---------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------

def get_steuersatz_for_category(kategorie: str) -> str:
    """
    Gibt den vorgeschlagenen Steuersatz für eine Kategorie zurück.
    Falls die Kategorie nicht bekannt ist → Standard: 19%
    """
    return KATEGORIE_STEUER.get(kategorie, "19")


def berechne_netto_und_mwst(brutto: float, steuersatz_key: str) -> tuple:
    """
    Berechnet Netto und MwSt aus einem Bruttobetrag.
    Rückgabe: (netto, mwst_betrag)
    """
    satz = STEUERSAETZE.get(steuersatz_key, 0.19)
    netto = brutto / (1 + satz)
    mwst = brutto - netto
    return round(netto, 2), round(mwst, 2)
