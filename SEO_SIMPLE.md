# Simple SEO Setup - NethZ Django App

## ✅ What's implemented (essentials only)

### 1. Dynamic Sitemap.xml

- **URL**: `/sitemap.xml`
- Automatically generates from your URLs and database
- Updates when you add new TM semesters or worldle regions
- No maintenance required

### 2. robots.txt

- **URL**: `/robots.txt`
- Tells search engines what to crawl
- Blocks admin areas, allows important pages

### 3. Translated Meta Tags

- **Titles**: "Enzo Baraldi", "Engineering Mechanics HS24", "Worldle"
- **Descriptions**: Short, helpful descriptions for search results
- **Keywords**: Basic keywords for search engines
- **Fully translated**: English originals, German translations

## 🧪 Test your setup

```bash
# Quick SEO check (simple output)
python manage.py validate_seo

# View sitemap (22+ URLs automatically generated)
curl http://localhost:8000/sitemap.xml

# View robots.txt
curl http://localhost:8000/robots.txt
```

## 🌍 What you get (both languages)

### Home page:

- **English**: "Enzo Baraldi" + "Engineering mechanics study materials and geography games for ETH Zurich students"
- **German**: "Enzo Baraldi" + "Technische Mechanik Studienunterlagen und Geografie-Spiele für ETH Zürich Studenten"

### TM pages:

- **English**: "Engineering Mechanics HS24" + "Engineering mechanics study materials and solutions for ETH Zurich students"
- **German**: "Technische Mechanik HS24" + "Technische Mechanik Studienunterlagen und Lösungen für ETH Zürich Studenten"

### Worldle pages:

- **English**: "Worldle" + "Geography games - guess capitals, languages, currencies and countries"
- **German**: "Worldle" + "Geografie-Spiele - errate Hauptstädte, Sprachen, Währungen und Länder"

## 🔄 Translation commands (when you add new SEO text)

```bash
# 1. Extract new translatable strings
python manage.py makemessages -l de

# 2. Edit translations in: locale/de/LC_MESSAGES/django.po

# 3. Compile translations
python manage.py compilemessages -l de
```

## 🚀 For production

1. **Submit sitemap to Google**: Go to [Google Search Console](https://search.google.com/search-console) and submit `https://yourdomain.com/sitemap.xml`

2. **Set production domain**: Add to your environment:
   ```
   PRODUCTION_DOMAINS=yourdomain.com
   ```

## 📝 Adding new content

**New TM semester**: Just add to database - appears automatically in sitemap

```python
ExerciseSession.objects.create(
    short_name="TM_FS25",
    name="Engineering Mechanics FS25"
)
```

**New static page**: Add to `nethz_django/sitemaps.py` in `StaticViewSitemap.items()`

## ✅ Current status

- **Sitemap**: ✅ Dynamic (22+ URLs from DB + country data)
- **robots.txt**: ✅ Configured
- **Meta tags**: ✅ Simple and clean
- **Translations**: ✅ English + German
- **No bloat**: ❌ No Open Graph, Twitter Cards, or JSON-LD

That's it! Clean, simple, and search engine friendly.
