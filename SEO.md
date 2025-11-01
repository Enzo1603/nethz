# SEO-Konfiguration

## Übersicht

Die Website ist für Google-Indexierung optimiert mit:
- **robots.txt**: Dynamisch generiert, blockiert nur private Bereiche
- **sitemap.xml**: Automatisch generiert, enthält alle Seiten in beiden Sprachen (de + en)
- **Zweisprachig**: Jede Seite wird für Deutsch und Englisch indexiert

## Wie es funktioniert

### robots.txt (`/robots.txt`)
- Wird dynamisch durch `nethz_django/views.py` generiert
- Enthält korrekte Domain und Sitemap-URL
- Blockiert: `/admin/`, `/de/accounts/`, `/en/accounts/`
- Erlaubt: Alle anderen wichtigen Seiten

### sitemap.xml (`/sitemap.xml`)
- Wird durch `nethz_django/sitemaps.py` generiert
- **44 URLs total** (22 Deutsch + 22 Englisch)
- Beinhaltet:
  - Statische Seiten (Home, Worldle, etc.)
  - TM Semester (automatisch aus Datenbank)
  - Worldle Regionen (automatisch aus Code)

### Automatische Updates
- **TM Semester**: Neue Semester mit `TM_` Prefix werden automatisch zur Sitemap hinzugefügt
- **Worldle Regionen**: Werden aus `worldle/country_data.py` gelesen
- **Keine manuelle Wartung nötig**

## Deployment

```bash
# 1. Code deployen
git push

# 2. Auf Server aktualisieren
ssh server
cd /path/to/nethz
git pull
source .venv/bin/activate
sudo systemctl restart gunicorn

# 3. Validieren
curl https://nethz.baraldi.ch/robots.txt
curl https://nethz.baraldi.ch/sitemap.xml | head -50
```

## Google Search Console

1. **Sitemap einreichen**:
   - Gehe zu: https://search.google.com/search-console
   - Sitemaps → Neue Sitemap hinzufügen
   - URL: `https://nethz.baraldi.ch/sitemap.xml`

2. **robots.txt testen**:
   - Einstellungen → robots.txt-Tester
   - Prüfen dass wichtige URLs erlaubt sind

3. **Coverage überwachen**:
   - Nach 2-4 Wochen sollte "Indexiert" steigen
   - "Gecrawlt aber nicht indexiert" sollte sinken

## Erwartungen

- **Woche 1-2**: Google crawlt die Sitemap
- **Woche 2-4**: Erste URLs werden indexiert (~20-30)
- **Monat 2-3**: Vollständige Indexierung (~40-44 URLs)

## Dateien

### Geändert/Neu:
- `nethz_django/views.py` - robots.txt View
- `nethz_django/sitemaps.py` - i18n-Unterstützung mit `I18nSitemap`
- `nethz_django/urls.py` - Verwendet robots.txt View

### Kann gelöscht werden:
- `templates/robots.txt` - Nicht mehr verwendet

## Troubleshooting

### URLs testen
```bash
# Lokal
python manage.py runserver
curl http://localhost:8000/robots.txt
curl http://localhost:8000/sitemap.xml

# Production
curl https://nethz.baraldi.ch/robots.txt
curl https://nethz.baraldi.ch/sitemap.xml
```

### Häufige Probleme
- **"Gecrawlt aber nicht indexiert"**: Normal bei neuen Websites, 2-4 Wochen warten
- **"Durch robots.txt blockiert"**: Nur `/admin/` und `/*/accounts/` sollten blockiert sein
- **Fehlende URLs**: Django Check durchführen: `python manage.py check`

## Neue Inhalte hinzufügen

### Neues TM Semester (automatisch)
```python
ExerciseSession.objects.create(
    short_name="TM_FS25",
    name="Technische Mechanik FS25"
)
# → Erscheint automatisch in Sitemap!
```

### Neue statische Seite (manuell)
In `nethz_django/sitemaps.py` → `StaticViewSitemap.items()`:
```python
return [
    "main:home",
    "main:neue_seite",  # Hinzufügen
    # ...
]
```

Das war's! Simple und wartungsfrei. 🚀
