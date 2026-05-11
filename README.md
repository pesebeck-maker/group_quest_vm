# group_quest_vm

Eine Streamlit-App, mit der Gruppen gemeinsam an Challenges dranbleiben.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Die SQLite-Datei `groupquest.db` wird beim ersten Start automatisch erzeugt.

## Sprint-Historie

**Sprint 1 (Click-Dummy, ohne Backend)**
- US-33 Registrierung
- US-32 Login / Logout
- US-14 Challenge erstellen
- US-16 Challenges auflisten

**Sprint 2 (Click-Dummy, ohne Backend)**
- US-17 Challenge beitreten / verlassen
- US-18 Check-in dokumentieren
- US-29 Multi-Page-Navigation

**Sprint 3 (Backend-Integration für Nutzerverwaltung)**
- Backend zu US-33 Registrierung
- Backend zu US-32 Login / Logout

**Sprint 4 (Backend-Integration für Inhalte)**
- Backend zu US-14 Challenge erstellen
- Backend zu US-16 Challenges auflisten
- Backend zu US-17 Challenge beitreten / verlassen
- Backend zu US-18 Check-in dokumentieren

## Projektstruktur

```
.
├── app.py              # Streamlit-UI (Sprint 1 + 2, ergänzt in Sprint 3 + 4)
├── database.py         # SQLite-Funktionen (Sprint 3 + 4)
├── requirements.txt
└── groupquest.db       # wird zur Laufzeit erzeugt
```

## SCRUM-Rollen

- **Product Owner:** Adrian Hörburger
- **Scrum Master:** Philipp Freiherr von Esebeck
- **Entwicklungsteam:** Lovis Albrecht, Anton Eitenbichler, Henri Hoffmann, Adrian Hell