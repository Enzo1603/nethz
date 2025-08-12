# Nethz Django Application

A minimal Django web application with automated semantic versioning and Docker deployment.

## 🚀 Quick Start

```bash
git clone <your-repo-url>
cd nethz
cp .env.example .env
# Edit .env with your actual values
./deploy.sh
```

Application runs at http://localhost:8000

## 🔄 Automated Release Workflow

### Conventional Commits → Automatic Releases

```bash
# Make changes and commit with conventional format
git commit -m "fix: button alignment issue"      # → PATCH (2.0.0 → 2.0.1)
git commit -m "feat: add user dashboard"         # → MINOR (2.0.0 → 2.1.0)
git commit -m "feat!: redesign API"              # → MAJOR (2.0.0 → 3.0.0)
git push origin main
```

→ GitHub Actions automatically:

1. Analyzes commit messages
2. Bumps version in `pyproject.toml`
3. Creates git tag
4. Builds Docker image
5. Pushes to Docker Hub with version + `latest` tags

### Commit Types

| Prefix                               | Version Bump | Example                            |
| ------------------------------------ | ------------ | ---------------------------------- |
| `fix:`                               | PATCH        | `fix: resolve login bug`           |
| `feat:`                              | MINOR        | `feat: add email notifications`    |
| `feat!:`, `fix!:`                    | MAJOR        | `feat!: new authentication system` |
| `docs:`, `style:`, `test:`, `chore:` | PATCH        | `docs: update README`              |

## 🛠️ Available Commands

### Local Development

```bash
./build.sh                 # Build image locally for testing (auto-detects sudo)
./deploy.sh                # Run locally with docker compose (auto-detects sudo)
```

### Manual Docker Commands

```bash
# Run locally (use sudo if needed for your system)
docker compose up -d --build

# View logs
docker compose logs -f

# Stop
docker compose down
```

## 🔧 Environment Variables

Create `.env` file from `.env.example`:

| Variable              | Required | Description                                               |
| --------------------- | -------- | --------------------------------------------------------- |
| `SECRET_KEY`          | ✅       | Django secret key ([generate here](https://djecrety.ir/)) |
| `PRODUCTION_DOMAINS`  | ✅\*     | Your domain(s), comma-separated                           |
| `EMAIL_HOST`          | ✅       | SMTP server (e.g., smtp.gmail.com)                        |
| `EMAIL_PORT`          | ✅       | SMTP port (e.g., 587)                                     |
| `EMAIL_HOST_USER`     | ✅       | SMTP username                                             |
| `EMAIL_HOST_PASSWORD` | ✅       | SMTP password                                             |
| `DEFAULT_FROM_EMAIL`  | ✅       | Default sender email                                      |

\*Required only in production

## 🔄 CI/CD Setup

### GitHub Secrets Required

Add to your GitHub repository settings:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

### How It Works

1. **Push to main** → Analyzes commits → Determines version bump
2. **Updates** `pyproject.toml` with new version
3. **Creates** git tag automatically
4. **Builds** Docker image with semantic version
5. **Pushes** to Docker Hub as `username/nethz:x.y.z` and `latest`

## 🗄️ Database & Storage

- **Database**: SQLite (perfect for small deployments)
- **Location**: `db/db.sqlite3` (persisted via Docker volumes)
- **Static Files**: Collected during build, served via WhiteNoise

## 📁 Key Files

```
nethz/
├── docker-compose.yml          # Local development
├── Dockerfile                  # Container definition
├── deploy.sh                   # Local deployment
├── build.sh                    # Local build script
├── .env.example               # Environment template
├── pyproject.toml             # Version source of truth
└── .github/workflows/docker.yml # CI/CD pipeline
```

## 🚨 Troubleshooting

### Application won't start

- Check `.env` file configuration
- View logs: `docker compose logs`

### Database issues

- Reset database: `rm -rf db/db.sqlite3` (recreates on restart)

### Email not working

- Verify SMTP credentials in `.env`
- For Gmail: Use app-specific password
- Check EMAIL_USE_TLS setting

### Port conflicts

Change port in docker-compose.yml:

```yaml
ports:
  - "8080:8000" # Use 8080 instead of 8000
```

## 🔒 Security Features

- Non-root user in Docker container
- Environment variables for sensitive data
- Multi-stage Docker build
- Minimal Python slim base image
- Health checks included

## 📝 Example Workflow

```bash
# Development cycle
git checkout -b feature/new-dashboard
# Make changes...
git commit -m "feat: add user dashboard with analytics"
git push origin feature/new-dashboard
# Create PR, merge to main

# Automatic release triggered:
# - Sees "feat:" → minor version bump
# - 2.0.0 → 2.1.0
# - Docker image built and pushed
# - Ready for production use
```

## 🐳 Docker Notes

Scripts automatically detect if `sudo` is needed for Docker commands and adapt accordingly. Works on systems that require `sudo docker` and those that don't.

The `latest` tag always points to the most recent stable release.
