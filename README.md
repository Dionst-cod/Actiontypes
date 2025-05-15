# Actiontypes — Werkplaats 3 (Inhaalopdracht 2023/2024)

Deze applicatie is gebouwd als onderdeel van Werkplaats 3 (WP3) voor de opleiding Software Development. De webapplicatie bepaalt het "action type" van studenten op basis van 20 stellingen, beheert studentgegevens en ondersteunt docenten bij het vormen van gebalanceerde teams.

---

## Functionaliteiten

### Studenten

- Voeren hun studentnummer in
- Beantwoorden 20 stellingen één voor één (AJAX)
- Kunnen het formulier slechts één keer invullen
- Actiontype wordt automatisch berekend (zoals INFP, ESTJ, enz.)

## Test Login Gegevens

**Docent (admin):**

- Gebruikersnaam: `admin`
- Wachtwoord: `admin123`

### Docenten

- Loggen in met gebruikersnaam en wachtwoord
- Zien alle studenten, actiontypes en voortgang
- Kunnen studenten toevoegen, resetten, en filteren op klas/team
- Kunnen een CSV exporteren met alle resultaten
- Admins kunnen docenten toevoegen met admin rechten

---

## Technische Specificaties

- **Framework:** Flask (Python 3.11)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **Backend:** REST API (GET + POST)
- **Structuur:** MVC volgens PEP8-standaarden

---

## Installatie-instructies

### Benodigdheden

- Python 3.11

### Installatie

```bash
# 1. Maak een virtuele omgeving aan
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Installeer de dependencies
pip install -r requirements.txt

# 3. Start de applicatie
flask run
```

## Belangrijke URL's

| Pagina                 | URL                                  | Omschrijving                        |
| ---------------------- | ------------------------------------ | ----------------------------------- |
| Student-invulpagina    | http://localhost:5000/student        | Voor studenten die de test invullen |
| Docenten login         | http://localhost:5000/login          | Loginpagina voor docenten           |
| Docenten dashboard     | http://localhost:5000/admin          | Overzicht van studenten             |
| Docentenbeheer (admin) | http://localhost:5000/admin/teachers | Alleen zichtbaar voor admins        |
