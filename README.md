# Nethz Django Application

Minimal Django web app with smart Docker deployment.

## 🚀 Quick Start

```bash
git clone <your-repo-url>
cd nethz
cp .env.example .env
# Edit .env with your values
./deploy.sh
```

Application runs at http://localhost:8000

## 🛠️ Development Commands

```bash
./build.sh          # Build Docker image
./deploy.sh         # Deploy locally (auto-builds when needed)
```

Both scripts auto-detect if `sudo` is required for Docker.

## 🔧 Environment Setup

Create `.env` from `.env.example`:

```bash
SECRET_KEY=your-secret-key
PRODUCTION_DOMAINS=yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your@email.com
```

## 🔄 Automated Releases

Push with conventional commits for automatic versioning:

```bash
git commit -m "fix: button alignment"     # → 2.0.0 → 2.0.1 (patch)
git commit -m "feat: add dashboard"      # → 2.0.0 → 2.1.0 (minor)
git commit -m "feat!: redesign API"      # → 2.0.0 → 3.0.0 (major)
git push origin main
```

GitHub Actions automatically:

- Bumps version in `pyproject.toml`
- Creates git tag
- Builds and pushes Docker image to Docker Hub

## 🔧 Manual Docker Commands

```bash
docker compose up -d    # Start
docker compose logs -f  # View logs
docker compose down     # Stop
```

## 🗄️ Database

SQLite database persisted in `./db/` directory.

## 🚨 Troubleshooting

**Application won't start:** Check `.env` configuration and `docker compose logs`

**Database issues:** Remove `db/db.sqlite3` to reset

**Port conflicts:** Change port in `docker-compose.yml`

## 📁 Structure

```
nethz/
├── deploy.sh           # Smart deployment script
├── build.sh            # Build script
├── Dockerfile          # Multi-stage build
├── docker-compose.yml  # Local development
├── .env.example        # Environment template
└── pyproject.toml      # Version source of truth
```
