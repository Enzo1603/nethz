# SEO Implementation Guide für NethZ Django App

Diese Dokumentation erklärt die vollständige SEO-Implementierung für deine Django-Webseite.

## 🎯 Übersicht

Die SEO-Implementierung umfasst:

- ✅ Automatische Sitemap.xml Generierung
- ✅ Robots.txt für Suchmaschinen-Crawler
- ✅ Meta-Tags für bessere Indexierung
- ✅ Open Graph & Twitter Card Support
- ✅ Strukturierte Daten (JSON-LD)
- ✅ Mehrsprachige SEO-Unterstützung
- ✅ Management Commands für Testing

## 📁 Dateien-Struktur

```
nethz/
├── nethz_django/
│   ├── settings.py          # django.contrib.sitemaps hinzugefügt
│   ├── urls.py             # Sitemap & Robots URLs
│   └── sitemaps.py         # Dynamische Sitemap-Konfiguration (NEU)
├── lib/
│   ├── context_processors.py  # SEO-Defaults
│   └── seo_utils.py           # SEO-Hilfsfunktionen (NEU)
├── templates/
│   ├── seo_meta.html          # SEO Meta-Tags Fragment (NEU)
│   ├── robots.txt             # Robots.txt Template (NEU)
│   └── components/_base.html  # Aktualisiert mit SEO
├── main/management/commands/
│   └── validate_seo.py        # SEO-Validierungs-Command (NEU)
└── SEO_GUIDE.md              # Diese Datei
```

## 🚀 Schnellstart

### 1. Sitemap testen

```bash
python manage.py validate_seo --check-urls --verbose
```

### 2. URLs überprüfen

- **Sitemap**: http://localhost:8000/sitemap.xml
- **Robots**: http://localhost:8000/robots.txt

### 3. SEO in Views verwenden

```python
from lib.seo_utils import get_home_seo, add_seo_to_context

def my_view(request):
    context = {"my_data": "value"}

    # SEO-Daten hinzufügen
    seo_data = get_home_seo()
    add_seo_to_context(context, seo_data)

    return render(request, "my_template.html", context)
```

## 🔧 Konfiguration

### Dynamische Sitemap Features

Die Sitemap ist **vollständig dynamisch** und aktualisiert sich automatisch:

#### 📚 Technische Mechanik Semester

```python
# Automatisch aus der Datenbank geladen
def items(self):
    tm_sessions = ExerciseSession.objects.filter(
        short_name__startswith="TM_"
    )
    return [session.replace("TM_", "").lower() for session in tm_sessions]
```

#### 🌍 Worldle Regionen

```python
# Automatisch aus den Länder-Daten geladen
def items(self):
    return [region for region in VALID_REGIONS
            if region not in ['worldwide', 'antarctic']]
```

### Sitemap erweitern

**Neue statische Seiten hinzufügen** in `StaticViewSitemap`:

```python
def items(self):
    return [
        'main:home',
        'main:technische_mechanik',
        'main:neue_seite',  # <- Neue URL hier hinzufügen
        # ...
    ]
```

### SEO-Defaults ändern

**lib/context_processors.py** bearbeiten:

```python
def get_seo_defaults():
    return {
        'site_name': 'Dein Site Name',
        'default_title': 'Dein Standard Titel',
        'default_description': 'Deine Standard Beschreibung',
        # ...
    }
```

## 📝 Template Integration

### Basis Template (bereits implementiert)

```html
<!-- In components/_base.html -->
<head>
  <!-- SEO Meta Tags -->
  {% include "seo_meta.html" %}

  <title>{{ title|default:"NethZ - Enzo Baraldi" }}</title>
</head>
```

### Einzelne Templates optimieren

**Option 1: In der View (empfohlen)**

```python
def my_view(request):
    context = {}
    seo_data = SEOData(
        title="Mein Seitentitel",
        description="Meine Seitenbeschreibung",
        keywords="keyword1, keyword2"
    )
    add_seo_to_context(context, seo_data)
    return render(request, "template.html", context)
```

**Option 2: Im Template**

```html
{% extends "components/_base.html" %} {% block head %}
<!-- SEO Variablen setzen -->
{{ "Mein Titel"|add_to_context:"title" }} {{ "Meine
Beschreibung"|add_to_context:"meta_description" }} {% endblock %}
```

## 🎮 Verfügbare SEO-Hilfsfunktionen

```python
from lib.seo_utils import (
    get_home_seo,                    # Homepage SEO
    get_technische_mechanik_seo,     # TM Seiten
    get_worldle_home_seo,            # Worldle Hauptseite
    get_worldle_capitals_seo,        # Hauptstädte Quiz
    get_worldle_languages_seo,       # Sprachen Quiz
    get_worldle_competitive_seo,     # Wettkampf Modi
    get_leaderboards_seo,            # Bestenlisten
)
```

### Eigene SEO-Funktion erstellen

```python
def get_my_page_seo():
    return SEOData(
        title=_("Mein Seitentitel"),
        description=_("Meine Beschreibung"),
        keywords=_("meine, schlüsselwörter"),
        og_type='article',  # website, article, game
        structured_data_type='Article',  # WebSite, Course, Game
    )
```

## 🤖 Robots.txt anpassen

**templates/robots.txt** bearbeiten:

```
User-agent: *
Allow: /

# Neue Verzeichnisse blockieren
Disallow: /private/
Disallow: /internal/

# Neue Bereiche erlauben
Allow: /new-section/
```

## 📊 Monitoring & Testing

### Management Command verwenden

```bash
# Basis-Validierung
python manage.py validate_seo

# Mit URL-Tests (kann langsam sein)
python manage.py validate_seo --check-urls

# Detaillierte Ausgabe
python manage.py validate_seo --verbose

# Alles zusammen
python manage.py validate_seo --check-urls --verbose
```

### Manuelle Tests

1. **Sitemap**: `curl http://localhost:8000/sitemap.xml`
2. **Robots**: `curl http://localhost:8000/robots.txt`
3. **Meta-Tags**: Browser-Entwicklertools → `<head>`-Bereich inspizieren

### Production Testing Tools

- [Google Search Console](https://search.google.com/search-console)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [PageSpeed Insights](https://pagespeed.web.dev/)

### Sitemap-Inhalt prüfen

```bash
# Detaillierte Sitemap-Analyse
python manage.py validate_seo --verbose

# Zeigt Breakdown:
# 🏠 Static pages: 10
# 📚 TM semesters: 2  (aus Datenbank)
# 🌍 Worldle regions: 10  (aus country_data.py)
```

## 🌍 Mehrsprachigkeit

SEO-Templates unterstützen automatisch:

- **hreflang**: Sprachalternativen für Suchmaschinen
- **og:locale**: Open Graph Spracheinstellungen
- **Übersetzungen**: Alle SEO-Texte sind übersetzbar

```python
# In seo_utils.py verwende immer gettext
title=_("Mein Titel")  # ✅ Übersetzbar
title="Mein Titel"     # ❌ Nicht übersetzbar
```

## ⚡ Performance & Dynamik

- **Dynamische Updates**: Sitemap aktualisiert sich automatisch
  - Neue TM-Semester werden automatisch erkannt
  - Worldle-Regionen kommen aus den Länderdaten
  - Keine manuellen Updates nötig
- **Caching**: Sitemap wird automatisch gecacht
- **Lazy Loading**: SEO-Daten werden nur bei Bedarf geladen
- **Minimal Overhead**: Nur 1-2ms pro Request zusätzlich

### Automatische Erkennung:

```python
# Neue Semester hinzufügen - erscheinen automatisch in Sitemap
ExerciseSession.objects.create(
    short_name="TM_FS25",
    name="Engineering Mechanics FS25"
)
```

## 🔍 Erweiterte Features

### Custom Structured Data

```html
<!-- In deinem Template -->
{% block head %}
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "{{ course.name }}",
    "description": "{{ course.description }}"
  }
</script>
{% endblock %}
```

### Custom Meta Tags

```python
# In deiner View
context = {
    'canonical_url': 'https://example.com/canonical-version/',
    'og_image': 'https://example.com/image.jpg',
    'twitter_card': 'summary_large_image',
    'meta_robots': 'noindex, nofollow',  # Für private Seiten
}
```

## 🚨 Wichtige Hinweise

1. **Production Domains**: Stelle sicher, dass `PRODUCTION_DOMAINS` in den Settings korrekt gesetzt ist
2. **HTTPS**: Sitemap verwendet automatisch HTTPS in Production
3. **URL Updates**: Nach URL-Änderungen den Sitemap-Cache leeren
4. **Testing**: Teste immer mit dem Management Command vor Deployment

## 📈 SEO Checklist

- [ ] Sitemap.xml ist erreichbar und gültig
- [ ] Robots.txt ist konfiguriert
- [ ] Alle wichtigen Seiten haben eindeutige Titel
- [ ] Meta-Descriptions sind aussagekräftig (150-160 Zeichen)
- [ ] Keywords sind relevant und nicht übertrieben
- [ ] Open Graph Tags sind gesetzt
- [ ] Strukturierte Daten sind implementiert
- [ ] Hreflang für mehrsprachige Inhalte
- [ ] Canonical URLs bei doppelten Inhalten

## 🆘 Troubleshooting

### Sitemap leer?

- **Dynamische Sitemaps**: Prüfe ob Daten in DB vorhanden sind

```bash
# TM-Sessions prüfen
python manage.py shell -c "from main.models import ExerciseSession; print(list(ExerciseSession.objects.filter(short_name__startswith='TM_')))"

# Worldle-Regionen prüfen
python manage.py shell -c "from worldle.country_data import VALID_REGIONS; print(VALID_REGIONS)"
```

- Teste URLs mit `reverse()` im Django Shell

### 500 Fehler bei Sitemap?

- Prüfe Logs: `python manage.py runserver --verbosity=2`
- Validiere mit: `python manage.py validate_seo`

### Meta-Tags werden nicht angezeigt?

- Stelle sicher, dass `{% include "seo_meta.html" %}` im `<head>` steht
- Überprüfe Template-Kontext mit `{{ context|pprint }}`

### URLs in Sitemap fehlerhaft?

- Überprüfe `ALLOWED_HOSTS` und `PRODUCTION_DOMAINS`
- Teste mit verschiedenen `request.get_host()` Werten

---

**💡 Tipp**: Verwende regelmäßig `python manage.py validate_seo --verbose` um sicherzustellen, dass alles korrekt funktioniert!
