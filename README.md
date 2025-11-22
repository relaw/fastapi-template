# FastAPI Template

🚀 **Production-ready FastAPI template** with async PostgreSQL, Redis, Celery, and complete project structure.

---

## 🎯 Features

- ✅ **FastAPI** - Modern async web framework
- ✅ **PostgreSQL + AsyncPG** - Async database with SQLAlchemy 2.0
- ✅ **Redis** - Caching and Celery broker
- ✅ **Celery** - Background task processing
- ✅ **Alembic** - Database migrations
- ✅ **Pydantic Settings** - Environment variable management
- ✅ **Docker Compose** - Local development setup
- ✅ **Ready for Render** - Pre-configured for deployment

---

## 🚀 Quick Start (10 minutes)

### 1. Clone this template

```bash
git clone https://github.com/relaw/fastapi-template.git my-new-project
cd my-new-project
```

### 2. Update git remote

```bash
# Create new repo on GitHub first, then:
git remote set-url origin https://github.com/YOUR_USERNAME/my-new-project.git
git push -u origin main
```

### 3. Setup environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys and database URLs
```

### 4. Start local services

```bash
# Start PostgreSQL + Redis with Docker
docker-compose up -d

# Check services are running
docker-compose ps
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal: Start Celery worker
celery -A app.tasks.worker worker --loglevel=info
```

### 7. Test it works

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # SQLAlchemy models
│   │   ├── order.py
│   │   ├── biznesplan.py
│   │   └── ...
│   ├── routes/              # API endpoints (add your routes here)
│   ├── services/            # Business logic (add your services here)
│   ├── tasks/               # Celery tasks
│   └── utils/               # Helper functions
├── config/
│   ├── settings.py          # Environment variables (Pydantic)
│   └── database.py          # Database connection
├── alembic/                 # Database migrations
├── static/                  # Static files (CSS, JS, images)
├── tests/                   # Test files
├── docker-compose.yml       # Local PostgreSQL + Redis
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── .python-version          # Python version (3.11.11)
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file with your configuration:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (add your own)
ANTHROPIC_API_KEY=your_key_here
PODIO_APP_TOKEN=your_token_here
# ... add more as needed
```

### Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

---

## 🐳 Docker Services

**Start services:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f postgres
docker-compose logs -f redis
```

---

## 🚀 Deploy to Render

### 1. Create services

- **Web Service**: FastAPI app
- **Background Worker**: Celery worker
- **PostgreSQL**: Managed database
- **Redis**: Managed cache (or use Upstash free tier)

### 2. Environment variables on Render

Set in Render dashboard:
- `DATABASE_URL` (from PostgreSQL service - use External URL)
- `REDIS_URL` (from Redis service or Upstash)
- Add your API keys

### 3. Build & Start commands

**Web Service:**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Background Worker:**
- Build: `pip install -r requirements.txt`
- Start: `celery -A app.tasks.worker worker --loglevel=info`

### 4. Run migrations on Render

After first deploy, open Shell on Web Service:
```bash
alembic upgrade head
```

---

## 🧪 Development

### Running Tests

```bash
pytest
pytest --cov=app tests/
```

### Code Quality

```bash
# Check code style
ruff check .

# Format code
ruff format .
```

---

## 📚 Key Dependencies

- **fastapi** `0.115.6` - Web framework
- **uvicorn** `0.34.0` - ASGI server
- **sqlalchemy** `2.0.35` - ORM
- **asyncpg** `0.30.0` - Async PostgreSQL driver
- **alembic** `1.14.0` - Database migrations
- **celery** `5.4.0` - Task queue
- **redis** `5.2.1` - Cache client
- **pydantic** `2.10.5` - Data validation
- **pydantic-settings** `2.7.1` - Settings management
- **httpx** `0.28.1` - Async HTTP client

---

## 🎓 Next Steps

1. **Add your routes** in `app/routes/`
2. **Add your services** in `app/services/`
3. **Add your models** in `app/models/`
4. **Create migrations** with `alembic revision --autogenerate`
5. **Add your tests** in `tests/`
6. **Update `requirements.txt`** when adding new dependencies

---

## 📖 Documentation

- **FastAPI**: https://fastapi.tiangolo.com
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/en/20/
- **Alembic**: https://alembic.sqlalchemy.org
- **Celery**: https://docs.celeryproject.org
- **Pydantic**: https://docs.pydantic.dev

---

## 📝 License

MIT License - feel free to use this template for any project!

---

## 💡 Tips

- **Always use `.env` for secrets** - never commit `.env` to git
- **Use async/await** for all I/O operations (database, API calls)
- **Run migrations** before deploying new versions
- **Monitor Celery tasks** with Flower or logs
- **Use `httpx` instead of `requests`** for async HTTP calls

---

**Created by**: [relaw](https://github.com/relaw)  
**Template Repo**: https://github.com/relaw/fastapi-template

Happy coding! 🚀

